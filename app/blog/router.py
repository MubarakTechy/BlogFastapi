from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.auth.dependencies import get_current_user

from app.blog.schemas import (
    BlogCreate,
    BlogUpdate,
    BlogResponse
)

from app.blog.service import (
    create_blog,
    get_all_blogs,
    get_blog_by_id,
    update_blog,
    delete_blog
)


router = APIRouter(
    prefix="/blogs",
    tags=["Blogs"]
)


@router.post(
    "",
    response_model=BlogResponse,
    status_code=status.HTTP_201_CREATED
)
def create_blog_post(
    blog_data: BlogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_blog(
        db,
        blog_data,
        current_user.id
    )


@router.get(
    "",
    response_model=list[BlogResponse]
)
def get_blogs(
    db: Session = Depends(get_db)
):
    return get_all_blogs(db)


@router.get(
    "/{blog_id}",
    response_model=BlogResponse
)
def get_blog(
    blog_id: int,
    db: Session = Depends(get_db)
):
    blog = get_blog_by_id(
        db,
        blog_id
    )

    if not blog:
        raise HTTPException(
            status_code=404,
            detail="Blog not found"
        )

    return blog


@router.put(
    "/{blog_id}",
    response_model=BlogResponse
)
def update_blog_post(
    blog_id: int,
    blog_data: BlogUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    blog = get_blog_by_id(
        db,
        blog_id
    )

    if not blog:
        raise HTTPException(
            status_code=404,
            detail="Blog not found"
        )

    if blog.author_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only update your own blog"
        )

    return update_blog(
        db,
        blog,
        blog_data
    )


@router.delete(
    "/{blog_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_blog_post(
    blog_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    blog = get_blog_by_id(
        db,
        blog_id
    )

    if not blog:
        raise HTTPException(
            status_code=404,
            detail="Blog not found"
        )

    if blog.author_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own blog"
        )

    delete_blog(db, blog)

    return None
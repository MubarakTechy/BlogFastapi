from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Admin

from app.auth.dependencies import (
    get_current_user,
    get_current_user_or_admin
)



from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    UploadFile,
    File,
    Form
)

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

from app.utils.image_upload import upload_image


router = APIRouter(
    prefix="/blogs",
    tags=["Blogs"]
)


# ==========================================
# CREATE BLOG
# Logged-in users can create blogs
# ==========================================

@router.post(
    "",
    response_model=BlogResponse,
    status_code=status.HTTP_201_CREATED
)
def create_blog_post(
    title: str = Form(...),
    content: str = Form(...),
    published: bool = Form(True),
    image: UploadFile | None = File(None),

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)
):

    image_url = None

    if image:

        try:
            image_url = upload_image(image.file)

        except Exception:
            raise HTTPException(
                status_code=400,
                detail="Invalid image or image upload failed"
            )

    blog_data = BlogCreate(
        title=title,
        content=content,
        published=published
    )

    return create_blog(
        db,
        blog_data,
        current_user.id,
        image_url
    )
# ==========================================
# GET ALL BLOGS
# Public
# ==========================================

@router.get(
    "",
    response_model=list[BlogResponse]
)
def get_blogs(
    db: Session = Depends(get_db)
):
    return get_all_blogs(db)


# ==========================================
# GET ONE BLOG
# Public
# ==========================================

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


# ==========================================
# UPDATE BLOG
# Owner OR Admin
# ==========================================

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

    # Normal user can only update their own blog
    # Admin can update any blog
    if not current_user.is_admin and blog.author_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only update your own blog"
        )

    return update_blog(
        db,
        blog,
        blog_data
    )

# ==========================================
# DELETE BLOG
# Owner OR Admin
# ==========================================
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

    # Normal user can only delete their own blog
    # Admin can delete any blog
    if not current_user.is_admin and blog.author_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own blog"
        )

    delete_blog(
        db,
        blog
    )

    return None
    # ADMIN
    if isinstance(current_user_or_admin, Admin):
        delete_blog(
            db,
            blog
        )
        return None

    # NORMAL USER
    if blog.author_id != current_user_or_admin.id:
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own blog"
        )

    delete_blog(
        db,
        blog
    )

    return None
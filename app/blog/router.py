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

from app.models import Blog

from app.auth.dependencies import get_current_admin

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
    tags=["Blog"]
)


# ==========================================
# CREATE BLOG
# ADMIN ONLY
# ==========================================

@router.post(
    "",
    response_model=BlogResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_blog(
    title: str = Form(...),
    content: str = Form(...),
    published: bool = Form(True),
    image: UploadFile | None = File(None),

    db: Session = Depends(get_db),

    current_admin=Depends(get_current_admin)
):

    image_url = None

    # Upload image if provided
    if image:

        try:
            image_url = upload_image(
                image.file
            )

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Image upload failed"
            )

    blog_data = BlogCreate(
        title=title,
        content=content,
        published=published
    )

    return create_blog(
        db=db,
        blog_data=blog_data,
        admin_id=current_admin.id,
        image_url=image_url
    )


# ==========================================
# GET ALL BLOGS
# PUBLIC
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
# PUBLIC
# ==========================================

@router.get(
    "/{blog_id}",
    response_model=BlogResponse
)
def get_single_blog(
    blog_id: int,
    db: Session = Depends(get_db)
):

    blog = get_blog_by_id(
        db,
        blog_id
    )

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found"
        )

    return blog


# ==========================================
# UPDATE BLOG
# ADMIN ONLY
# ==========================================

@router.put(
    "/{blog_id}",
    response_model=BlogResponse
)
def update_existing_blog(
    blog_id: int,

    blog_data: BlogUpdate,

    db: Session = Depends(get_db),

    current_admin=Depends(get_current_admin)
):

    blog = get_blog_by_id(
        db,
        blog_id
    )

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found"
        )

    # Only the admin who owns the blog
    # can update it.
    if blog.admin_id != current_admin.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to edit this blog"
        )

    return update_blog(
        db,
        blog,
        blog_data
    )


# ==========================================
# DELETE BLOG
# ADMIN ONLY
# ==========================================

@router.delete(
    "/{blog_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_existing_blog(
    blog_id: int,

    db: Session = Depends(get_db),

    current_admin=Depends(get_current_admin)
):

    blog = get_blog_by_id(
        db,
        blog_id
    )

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found"
        )

    # Only the admin who owns the blog
    # can delete it.
    if blog.admin_id != current_admin.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to delete this blog"
        )

    delete_blog(
        db,
        blog
    )

    return None
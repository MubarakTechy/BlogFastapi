from sqlalchemy.orm import Session

from app.models import Blog
from app.blog.schemas import BlogCreate, BlogUpdate


# ==========================================
# CREATE BLOG
# ==========================================

def create_blog(
    db: Session,
    blog_data: BlogCreate,
    admin_id: int,
    image_url: str | None = None
):
    blog = Blog(
        title=blog_data.title,
        content=blog_data.content,
        image_url=image_url,
        published=blog_data.published,
        admin_id=admin_id
    )

    db.add(blog)
    db.commit()
    db.refresh(blog)

    return blog


# ==========================================
# GET ALL BLOGS
# ==========================================

def get_all_blogs(db: Session):
    return db.query(Blog).order_by(
        Blog.created_at.desc()
    ).all()


# ==========================================
# GET ONE BLOG
# ==========================================

def get_blog_by_id(
    db: Session,
    blog_id: int
):
    return db.query(Blog).filter(
        Blog.id == blog_id
    ).first()


# ==========================================
# UPDATE BLOG
# ==========================================

def update_blog(
    db: Session,
    blog: Blog,
    blog_data: BlogUpdate
):
    update_data = blog_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(blog, key, value)

    db.commit()
    db.refresh(blog)

    return blog


# ==========================================
# DELETE BLOG
# ==========================================

def delete_blog(
    db: Session,
    blog: Blog
):
    db.delete(blog)
    db.commit()
from sqlalchemy.orm import Session
from .models import Post
from .schemas import PostUpdate
from typing import Dict

def create_post_from_external(db: Session, external_data: Dict):
    post = Post(
        external_id=external_data["id"],
        title=external_data["title"],
        body=external_data["body"],
        source="jsonplaceholder"
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()

def update_post(db: Session, post_id: int, update_data: PostUpdate):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        if update_data.title is not None:
            post.title = update_data.title
        if update_data.body is not None:
            post.body = update_data.body
        db.commit()
        db.refresh(post)
    return post

def delete_post(db: Session, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        db.delete(post)
        db.commit()
        return True
    return False

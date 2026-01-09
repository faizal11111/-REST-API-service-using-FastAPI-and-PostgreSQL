from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas, external_client
from .deps import get_db

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/", response_model=schemas.PostRead, status_code=201)
async def create_post(post_create: schemas.PostCreate, db: Session = Depends(get_db)):
    try:
        external_data = await external_client.fetch_external_post(post_create.external_post_id)
    except external_client.ExternalAPIError as e:
        raise HTTPException(status_code=502, detail=str(e))
    post = crud.create_post_from_external(db, external_data)
    return post

@router.get("/{post_id}", response_model=schemas.PostRead)
def read_post(post_id: int, db: Session = Depends(get_db)):
    post = crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/{post_id}", response_model=schemas.PostRead)
def update_post(post_id: int, post_update: schemas.PostUpdate, db: Session = Depends(get_db)):
    post = crud.update_post(db, post_id, post_update)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_post(db, post_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"detail": "Post deleted"}

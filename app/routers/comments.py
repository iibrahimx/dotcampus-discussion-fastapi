from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.dependencies import get_current_user, get_db

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post(
    "/discussion/{discussion_id}",
    response_model=schemas.CommentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_comment(
    discussion_id: int,
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    discussion = (
        db.query(models.Discussion)
        .filter(models.Discussion.id == discussion_id)
        .first()
    )

    if not discussion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Discussion not found",
        )

    new_comment = models.Comment(
        content=comment.content,
        user_id=current_user.id,
        discussion_id=discussion_id,
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment


@router.get("/discussion/{discussion_id}", response_model=list[schemas.CommentResponse])
def get_comments_for_discussion(
    discussion_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    discussion = (
        db.query(models.Discussion)
        .filter(models.Discussion.id == discussion_id)
        .first()
    )

    if not discussion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Discussion not found",
        )

    comments = (
        db.query(models.Comment)
        .filter(models.Comment.discussion_id == discussion_id)
        .all()
    )

    return comments


@router.delete("/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )

    can_delete = current_user.role == "admin" or comment.user_id == current_user.id

    if not can_delete:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to delete this comment",
        )

    db.delete(comment)
    db.commit()

    return {"message": "Comment deleted successfully"}

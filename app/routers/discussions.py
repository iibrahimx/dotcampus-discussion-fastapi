from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.dependencies import get_current_user, get_db

router = APIRouter(prefix="/discussions", tags=["Discussions"])


@router.post(
    "/", response_model=schemas.DiscussionResponse, status_code=status.HTTP_201_CREATED
)
def create_discussion(
    discussion: schemas.DiscussionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    new_discussion = models.Discussion(
        title=discussion.title,
        content=discussion.content,
        owner_id=current_user.id,
    )

    db.add(new_discussion)
    db.commit()
    db.refresh(new_discussion)

    return new_discussion


@router.get("/", response_model=list[schemas.DiscussionResponse])
def get_all_discussions(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    discussions = db.query(models.Discussion).all()
    return discussions


@router.get("/{discussion_id}", response_model=schemas.DiscussionResponse)
def get_single_discussion(
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

    return discussion


@router.put("/{discussion_id}", response_model=schemas.DiscussionResponse)
def update_discussion(
    discussion_id: int,
    discussion_data: schemas.DiscussionUpdate,
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

    can_update = (
        current_user.role in ["mentor", "admin"]
        or discussion.owner_id == current_user.id
    )

    if not can_update:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to update this discussion",
        )

    discussion.title = discussion_data.title
    discussion.content = discussion_data.content

    db.commit()
    db.refresh(discussion)

    return discussion


@router.delete("/{discussion_id}")
def delete_discussion(
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

    can_delete = current_user.role == "admin" or discussion.owner_id == current_user.id

    if not can_delete:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to delete this discussion",
        )

    db.delete(discussion)
    db.commit()

    return {"message": "Discussion deleted successfully"}

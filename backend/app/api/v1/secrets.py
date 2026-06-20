from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, or_
from app.database import get_db
from app.models import Secret, User, AuditLog
from app.schemas import SecretCreate, SecretUpdate, SecretResponse, SecretListResponse
from app.core.security import get_current_user
from datetime import datetime

router = APIRouter(prefix="/api/v1/secrets", tags=["Secrets"])

@router.post("/", response_model=SecretResponse, status_code=status.HTTP_201_CREATED)
async def create_secret(
    secret: SecretCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new secret for the current user."""
    db_secret = Secret(
        owner_id=current_user.id,
        label=secret.label,
        encrypted_value=secret.encrypted_value,
        category=secret.category,
        metadata=secret.metadata
    )
    db.add(db_secret)

    # Log the action
    audit_log = AuditLog(
        user_id=current_user.id,
        secret_id=None,
        action="SECRET_CREATED"
    )
    db.add(audit_log)

    await db.commit()
    await db.refresh(db_secret)
    return db_secret

@router.get("/", response_model=list[SecretListResponse])
async def list_secrets(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    category: str = Query(None),
    search: str = Query(None)
):
    """List all secrets for the current user."""
    query = select(Secret).where(Secret.owner_id == current_user.id)

    if category:
        query = query.where(Secret.category == category)

    if search:
        query = query.where(Secret.label.ilike(f"%{search}%"))

    result = await db.execute(query)
    return result.scalars().all()

@router.get("/{secret_id}", response_model=SecretResponse)
async def get_secret(
    secret_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific secret."""
    result = await db.execute(
        select(Secret).where(
            and_(Secret.id == secret_id, Secret.owner_id == current_user.id)
        )
    )
    secret = result.scalar_one_or_none()

    if not secret:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Secret not found")

    # Log access
    audit_log = AuditLog(user_id=current_user.id, secret_id=secret_id, action="SECRET_READ")
    db.add(audit_log)
    await db.commit()

    return secret

@router.put("/{secret_id}", response_model=SecretResponse)
async def update_secret(
    secret_id: int,
    secret_update: SecretUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a secret."""
    result = await db.execute(
        select(Secret).where(
            and_(Secret.id == secret_id, Secret.owner_id == current_user.id)
        )
    )
    secret = result.scalar_one_or_none()

    if not secret:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Secret not found")

    update_data = secret_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(secret, key, value)

    secret.updated_at = datetime.utcnow()

    audit_log = AuditLog(user_id=current_user.id, secret_id=secret_id, action="SECRET_UPDATED")
    db.add(audit_log)

    await db.commit()
    await db.refresh(secret)
    return secret

@router.delete("/{secret_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_secret(
    secret_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a secret."""
    result = await db.execute(
        select(Secret).where(
            and_(Secret.id == secret_id, Secret.owner_id == current_user.id)
        )
    )
    secret = result.scalar_one_or_none()

    if not secret:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Secret not found")

    audit_log = AuditLog(user_id=current_user.id, secret_id=secret_id, action="SECRET_DELETED")
    db.add(audit_log)

    await db.delete(secret)
    await db.commit()

@router.post("/{secret_id}/favorite")
async def toggle_favorite(
    secret_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Toggle favorite status of a secret."""
    result = await db.execute(
        select(Secret).where(
            and_(Secret.id == secret_id, Secret.owner_id == current_user.id)
        )
    )
    secret = result.scalar_one_or_none()

    if not secret:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Secret not found")

    secret.is_favorite = not secret.is_favorite
    await db.commit()
    await db.refresh(secret)
    return secret

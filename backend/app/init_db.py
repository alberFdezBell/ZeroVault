"""Initialize database with admin user and sample data."""
import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import User, UserRole
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://zerovault_admin:zerovault_password@localhost:5432/zerovault_prod")

async def init_db():
    """Initialize database schema and insert initial data."""
    engine = create_async_engine(DATABASE_URL, echo=False)

    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)

    # Create session for data insertion
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        # Check if admin user already exists
        from sqlalchemy.future import select
        result = await session.execute(select(User).where(User.email == "admin@zerovault.local"))
        admin_exists = result.scalar_one_or_none()

        if not admin_exists:
            # Create admin user
            admin = User(
                email="admin@zerovault.local",
                auth_hash="admin_hash_demo_change_me_in_production",
                master_key_salt="f3a2c891e4b567d890abcdef1234567890abcdef1234567890abcdef12345678",
                encrypted_dek="encrypted_dek_demo",
                role=UserRole.ADMIN,
                is_active=True,
                requires_password_change=True
            )
            session.add(admin)
            await session.commit()
            print("✓ Admin user created: admin@zerovault.local")

        # Check if demo user exists
        result = await session.execute(select(User).where(User.email == "empleado@empresa.com"))
        demo_exists = result.scalar_one_or_none()

        if not demo_exists:
            # Create demo employee
            demo = User(
                email="empleado@empresa.com",
                auth_hash="hash_derivado_simulado_en_cliente_1234567890abcdef",
                master_key_salt="f3a2c891e4b567d890abcdef1234567890abcdef1234567890abcdef12345678",
                encrypted_dek="en_memoria_vault_key_blob_aes_gcm",
                role=UserRole.EMPLOYEE,
                is_active=True,
                requires_password_change=False
            )
            session.add(demo)
            await session.commit()
            print("✓ Demo user created: empleado@empresa.com")

    await engine.dispose()
    print("✓ Database initialized successfully")

if __name__ == "__main__":
    asyncio.run(init_db())

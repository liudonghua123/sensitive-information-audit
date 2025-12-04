import asyncio
import sys
import os

# Add the current directory to sys.path to ensure we can import app modules
sys.path.append(os.getcwd())

from app.db.session import AsyncSessionLocal
from app.core.security import get_password_hash
from app.db.models import User
from sqlalchemy.future import select

async def create_admin():
    async with AsyncSessionLocal() as db:
        # Check if user exists
        result = await db.execute(select(User).where(User.username == 'admin'))
        user = result.scalars().first()
        
        if user:
            print("Admin user already exists.")
            # Update password just in case
            user.hashed_password = get_password_hash('admin')
            db.add(user)
            await db.commit()
            print("Admin password updated.")
        else:
            print("Creating admin user...")
            new_user = User(
                username='admin',
                hashed_password=get_password_hash('admin'),
                is_superuser=True,
                is_active=True
            )
            db.add(new_user)
            await db.commit()
            print("Admin user created successfully.")

if __name__ == "__main__":
    try:
        asyncio.run(create_admin())
    except Exception as e:
        print(f"Error creating admin: {e}")

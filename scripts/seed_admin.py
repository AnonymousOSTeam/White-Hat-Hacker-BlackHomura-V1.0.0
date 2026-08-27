"""
Seed script to create an initial admin user with a temporary password.
Use only in development. Do NOT commit production secrets.
"""
from sqlmodel import Session, select
from app.db import engine
from app.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

TEMP_ADMIN_USERNAME = "admin"
TEMP_ADMIN_PASSWORD = "ChangeMe123!"

def seed_admin():
    with Session(engine) as session:
        existing = session.exec(select(User).where(User.username == TEMP_ADMIN_USERNAME)).first()
        if existing:
            print("✓ Admin user already exists")
            return
        admin = User(
            username=TEMP_ADMIN_USERNAME,
            hashed_password=get_password_hash(TEMP_ADMIN_PASSWORD),
            role="admin"
        )
        session.add(admin)
        session.commit()
        session.refresh(admin)
        print("✓ Created admin user")
        print(f"  username: {TEMP_ADMIN_USERNAME}")
        print(f"  temporary password: {TEMP_ADMIN_PASSWORD}")
        print("  ⚠️  IMPORTANT: Change this password on first login!")

if __name__ == "__main__":
    seed_admin()

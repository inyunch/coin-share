from sqlalchemy.orm import Session
from app.models import User, Role, Base
from app.database import engine, SessionLocal
from passlib.context import CryptContext

# Create the database tables if they don't exist
Base.metadata.create_all(bind=engine)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_admin_user():
    db: Session = SessionLocal()
    try:
        # Check if the admin user already exists
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            # Hash the password
            hashed_password = pwd_context.hash("admin_password")
            # Create a new admin user
            new_admin = User(username="admin", password_hash=hashed_password, name="Admin User", role=Role.ADMIN)
            db.add(new_admin)
            db.commit()
            db.refresh(new_admin)
            print("Admin user created with username: admin and password: admin_password")
        else:
            print("Admin user already exists.")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
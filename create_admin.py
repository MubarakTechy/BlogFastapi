from app.database import SessionLocal
from app.models import Admin
from app.auth.security import hash_password


db = SessionLocal()

email = "admin@gmail.com"
password = "MyStrongPassword@123"

existing_admin = db.query(Admin).filter(
    Admin.email == email
).first()

if existing_admin:
    print("Admin already exists!")
else:
    hashed_password = hash_password(password)

    admin = Admin(
        email=email,
        hashed_password=hashed_password
    )

    db.add(admin)
    db.commit()

    print("Admin created successfully!")
    print(f"Email: {email}")
    print(f"Password: {password}")

db.close()
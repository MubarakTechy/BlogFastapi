from app.database import SessionLocal
from app.auth.service import hash_password
from app.models import User


db = SessionLocal()

email = "admin@gmail.com"
username = "admin"
password = "MyStrongPassword@123"


existing_user = db.query(User).filter(
    User.email == email
).first()

if existing_user:
    print("Admin user already exists.")
else:

    hashed_password = hash_password(password)

    user = User(
        username=username,
        email=email,
        password=hashed_password,
        is_admin=True
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    print("Admin user created successfully!")
    print("User ID:", user.id)
    print("Email:", user.email)


db.close()
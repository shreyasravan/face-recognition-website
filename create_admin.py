from database import SessionLocal
import models

db = SessionLocal()

admin = models.User(
    name="Admin",
    email="shreyasravan92@gmail.com",
    password="admin@123",
    role="admin"
)

db.add(admin)
db.commit()

print("Admin user created!")
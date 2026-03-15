from database import SessionLocal
import models

db = SessionLocal()

teacher = models.User(
    name="Teacher1",
    email="teacher@gmail.com",
    password="teacher123",
    role="teacher"
)

db.add(teacher)
db.commit()

print("Teacher user created!")
from app.database import Base, SessionLocal, engine
from app.models import Student

Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    if db.query(Student).count() == 0:
        db.add_all(
            [
                Student(
                    name="Sanika Fulari",
                    email="sanika.demo@example.com",
                    phone="9999999999",
                    college="N.K. Orchid College of Engineering and Technology",
                    branch="Artificial Intelligence and Data Science",
                    year="TY",
                    skills="Python, SQL, Data Analysis, Machine Learning",
                ),
                Student(
                    name="Rahul Patil",
                    email="rahul.demo@example.com",
                    phone="9999999998",
                    college="Demo Engineering College",
                    branch="Computer Science",
                    year="TY",
                    skills="Java, DSA, SQL",
                ),
                Student(
                    name="Priya Deshmukh",
                    email="priya.demo@example.com",
                    phone="9999999997",
                    college="Demo Engineering College",
                    branch="Artificial Intelligence and Data Science",
                    year="SY",
                    skills="Python, Machine Learning, NLP",
                ),
            ]
        )
        db.commit()
        print("Seeded 3 sample students.")
    else:
        print("Student data already exists; no seed performed.")
finally:
    db.close()

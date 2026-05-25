from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session
import pymysql

# -------------------------
# DATABASE SETUP (MySQL)
# -------------------------
DB_USER = "root"
DB_PASS = "s@m0506"
DB_HOST = "localhost"
DB_NAME = "student_records"

# First, connect without a database to create it if it doesn't exist
try:
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS)
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    conn.commit()
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error creating database: {e}")

import urllib.parse
# Now connect to the specific database using SQLAlchemy
encoded_password = urllib.parse.quote_plus(DB_PASS)
URL = f"mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}/{DB_NAME}"

engine = create_engine(URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    studentName = Column(String(255), primary_key=True)
    studentAge = Column(Integer)
    studentstandard = Column(String(255))

# Create tables if they don't exist
Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------
# FASTAPI APP
# -------------------------
app = FastAPI()  
tasks = []

class Task(BaseModel):
    title : str
    description : str

@app.get("/")
def home():
    return {"message": "Hello World"}

# --- TASK ROUTES ---
@app.post("/tasks")
def createTask(newtask:Task):
    tasks.append(newtask)
    return {"message": "Task created successfully","task": newtask}

@app.get("/tasks")
def readTasks():
    return tasks

@app.put("/tasks/{task_id}")
def updateTask(task_id: int, updated_task: Task):
    if task_id<0 or task_id >= len(tasks):
        return {"error": "task not found"}
    tasks[task_id] = updated_task
    return {"message": "task updated successfully", "task": updated_task}

@app.delete("/tasks/{task_id}")
def deleteTask(task_id: int):
   if task_id >= len(tasks):
       return {"message":"invalid task id selection"}
   deletetask = tasks.pop(task_id)
   return {"message": "task seleted " , "task":deletetask}

# --- STUDENT ROUTES ---
class StudentCreate(BaseModel):
    studentName: str
    studentAge: int
    studentstandard: str

@app.post("/students")
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    new_student = Student(
        studentName=student.studentName,
        studentAge=student.studentAge,
        studentstandard=student.studentstandard
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return {"message": f"student {student.studentName} added!"}

@app.get("/students")
def read_students(db: Session = Depends(get_db)):
    return db.query(Student).all()
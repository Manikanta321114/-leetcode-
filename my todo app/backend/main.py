
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import sqlite3
import os

app = FastAPI()

# CORS – frontend ಗೆ backend access ಮಾಡಲು allow ಮಾಡ್ತದೆ
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # development time only; later specific origin use ಮಾಡು
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Data Models ----------

class Task(BaseModel):
    id: int
    text: str

class TaskCreate(BaseModel):
    text: str


# ---------- Database helpers (SQLite) ----------

DB_FILE = "todo.db"


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # to access columns by name
    return conn


def init_db():
    """Create table if not exists."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL
        );
        """
    )
    conn.commit()
    conn.close()


def seed_default_tasks():
    """First time default tasks insert ಮಾಡೋದು (table empty ಇದ್ದರೆ)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) AS cnt FROM tasks;")
    count = cur.fetchone()["cnt"]
    if count == 0:
        cur.executemany(
            "INSERT INTO tasks (text) VALUES (?);",
            [
                ("Learn FastAPI backend",),
                ("Connect frontend to API",),
            ],
        )
        conn.commit()
    conn.close()


# ---------- FastAPI events ----------

@app.on_event("startup")
def startup_event():
    # app start ಆಗುವಾಗ database + table ready ಮಾಡೋದು
    init_db()
    seed_default_tasks()


# ---------- Routes / Endpoints ----------

# 1) Get all tasks
@app.get("/tasks", response_model=List[Task])
def get_tasks():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, text FROM tasks ORDER BY id;")
    rows = cur.fetchall()
    conn.close()

    return [Task(id=row["id"], text=row["text"]) for row in rows]


# 2) Create new task
@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: TaskCreate):
    if not task.text.strip():
        raise HTTPException(status_code=400, detail="Task text is required")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (text) VALUES (?);", (task.text,))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()

    return Task(id=new_id, text=task.text)


# 3) Delete a task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = ?;", (task_id,))
    deleted = cur.rowcount
    conn.commit()
    conn.close()

    if deleted == 0:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task deleted"}

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
app = FastAPI(title='To-Do-Service')

class Task(BaseModel):
    title: str
    completed: bool = False

# tasks = {}
task_id_counter = 1

conn = sqlite3.connect('tasks.db', check_same_thread=False)
cur = conn.cursor()
cur.execute("""
            DROP TABLE IF EXISTS tasks
           """)
cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            description TEXT NOT NULL,
            completed BOOLEAN DEFAULT FALSE)
            """)
conn.commit()


@app.post("/task")
def create_task(task: Task):
    global task_id_counter
    cur.execute("INSERT INTO tasks (id, description, completed) VALUES (?, ?, ?)", 
                (task_id_counter, task.title, task.completed))
    conn.commit()
    # tasks[task_id_counter] = task
    task_id_counter += 1

    return {'id': task_id_counter - 1, 'task': task}

@app.get("/tasks")
def get_all_tasks():
    tasks = {}
    for i in range(1, task_id_counter):
        cur.execute("SELECT description, completed from tasks WHERE id = ?", (i,))
        row = cur.fetchone()
        if row is not None:
            title, completed = row
            dic = {'id': i, 'title': title, 'completed': completed}
            tasks[i] = dic

    return tasks


@app.get("/tasks/{id}")
def get_task(id: int):
    cur.execute("SELECT description, completed FROM tasks WHERE id = ?", (id,))
    row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")
    title, completed = row
    return {'id': id, 
            'title': title,
            'completed': completed}

@app.put("/tasks/{id}")
def put_task(id: int, updated_task: Task):
    cur.execute("SELECT description, completed FROM tasks WHERE id = ?", (id,))
    row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Task for update not found")
    cur.execute("UPDATE tasks set description = ?, completed = ? WHERE id = ?", 
                (updated_task.title, updated_task.completed, id))
    return {'id': id, 
            'title': updated_task.title,
            'completed': updated_task.completed}

@app.delete("/tasks/{id}")
def delete_task(id: int):
    cur.execute("SELECT description, completed FROM tasks WHERE id = ?", (id,))
    row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Task for delete not found")
    cur.execute("DELETE FROM tasks WHERE id = ?", (id,))
    return {'status': f'task {id} deleted'}
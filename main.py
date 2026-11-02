from fastapi import FastAPI
from models.types import TaskCreate
from rag.routes import router as rag_router

app = FastAPI();

app.include_router(rag_router)

tasks = [
    {
        "id": 1,
        "name":"first item",
        "status": "pending"
    },
    {
        "id": 2,
        "name":"second item",
        "status": "todo"
    },
    {
        "id": 3,
        "name":"third item",
        "status": "done"
    },
]

@app.get("/")
def home():
    return { "message": "Running the app server"}


@app.get("/task/{taskId}")
def getTask(taskId: int):
    return {"message": f"Requested task id is {taskId}"}

@app.get("/tasks")
def getTasks(status: str = None):
    if status == None:
        return tasks;
    return [task for task in tasks if task["status"] == status];

@app.post("/tasks", status_code=201)
def createTasks(task: TaskCreate, notify: bool = False):
    print(notify);
    tasks.append(task.model_dump());
    return task;

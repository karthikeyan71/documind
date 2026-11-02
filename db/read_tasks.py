from db.database import SessionLocal
from models.task_db import TaskDB
from sqlalchemy import select

with SessionLocal() as session:
    result = session.scalars(select(TaskDB)).all()

    for row in result:
        print(row.id, row.title, row.priority, row.status)
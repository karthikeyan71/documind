from sqlalchemy import text
from database import engine

with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM tasks ORDER BY id"))

    for row in result:
        print(row.id, row.title, row.priority, row.status)
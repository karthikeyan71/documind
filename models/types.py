from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    id: int = Field(ge=1, le=5)
    name: str = Field(min_length=5)
    status: str

class Task(BaseModel):
    id: int
    name: str
    status: str


class NestedOne(BaseModel):
    id: int
    tasks: list[Task]

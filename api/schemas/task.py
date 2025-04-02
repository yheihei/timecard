
from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    title: str = Field(None, example="クリーニングを取りに行く")


class Task(TaskBase):
    id: int
    done: bool = Field(False, description="完了フラグ")

    class Config:
        from_attributes = True


class TaskCreate(TaskBase):
    pass


class TaskCreateResponse(TaskCreate):
    id: int

    class Config:
        from_attributes = True

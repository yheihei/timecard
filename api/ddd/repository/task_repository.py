from sqlalchemy import select
from sqlalchemy.engine import Result

import api.models.task as task_model
from api.ddd.entity import Task
from api.ddd.repository.i_task_repository import ITaskRepository
from api.ddd.value_object import TaskId, TaskTitle


class TaskRepository(ITaskRepository):

    async def create(self, task_entity: Task) -> Task:
        task_data_model = self.__to_fastapi_model(task_entity)
        self.db.add(task_data_model)
        await self.db.commit()
        await self.db.refresh(task_data_model)
        return self.__to_entity(task_data_model, False)
    
    async def get_tasks_with_done(self) -> list[Task]:
        result: Result = await (
            self.db.execute(
                select(
                    task_model.Task,
                    task_model.Done.id.isnot(None).label("done"),
                ).outerjoin(task_model.Done)
            )
        )
        tasks: list[Task] = []
        task_data_model: task_model.Task
        done: bool
        for task_data_model, done in result.all():
            tasks.append(self.__to_entity(task_data_model, done))
        return tasks
    
    async def get_task(self, id: int) -> Task:
        result: Result = await (
            self.db.execute(
                select(
                    task_model.Task,
                    task_model.Done.id.isnot(None).label("done"),
                ).outerjoin(task_model.Done)
                .where(task_model.Task.id == id)
            )
        )
        task_data_model: task_model.Task
        done: bool
        task_data_model, done = result.one()
        return self.__to_entity(task_data_model, done)
    
    async def save(self, task_entity: Task) -> Task:
        result: Result = await (
            self.db.execute(
                select(
                    task_model.Task,
                    task_model.Done.id.isnot(None).label("done"),
                ).outerjoin(task_model.Done)
                .where(task_model.Task.id == task_entity.id.value())
            )
        )
        task_data_model: task_model.Task
        done: bool
        task_data_model, done = result.one()
        task_data_model.title = task_entity.title.value()
        self.db.add(task_data_model)
        await self.db.commit()
        await self.db.refresh(task_data_model)
        return self.__to_entity(task_data_model, done)
    
    def __to_fastapi_model(self, task_entity: Task) -> task_model.Task:
        return task_model.Task(id=task_entity.id.value(), title=task_entity.title.value())
    
    def __to_entity(self, task_data_model: task_model.Task, done: bool) -> Task:
        task_id = TaskId(int(task_data_model.id))
        task_title = TaskTitle(str(task_data_model.title))
        return Task(id=task_id, title=task_title, done=done)

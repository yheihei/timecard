
from sqlalchemy.ext.asyncio import AsyncSession

import api.models.task as task_model


async def delete_task(db: AsyncSession, original: task_model.Task):
    await db.delete(original)
    await db.commit()
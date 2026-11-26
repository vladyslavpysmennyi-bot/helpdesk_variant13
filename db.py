import os
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession
from sqlalchemy.orm import DeclarativeBase
engine=create_async_engine(os.getenv('DATABASE_URL','postgresql+asyncpg://helpdesk:helpdesk@postgres:5432/sla_db'))
Session=async_sessionmaker(engine,expire_on_commit=False)
class Base(DeclarativeBase): pass
async def get_db():
 async with Session() as s: yield s

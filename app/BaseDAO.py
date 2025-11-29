from .alembic.database import async_session_maker
from .alembic.models import Base
from sqlalchemy import select

class BaseDAO:
    model: Base = None

    @classmethod
    async def find_one_by_filter(cls, **filters) -> Base:
        async with async_session_maker() as session:
            comm = select(cls.model).filter_by(**filters)
            one = await session.scalar(comm)
            return one
    @classmethod
    async def add(cls, element: dict) -> Base:
        async with async_session_maker() as session:
            new_element = cls.model(**element)
            session.add(new_element)
            await session.commit()
            
        return new_element

        
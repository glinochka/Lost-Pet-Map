from ..alembic.database import async_session_maker
from ..alembic.models import Lost_report, Found_report, User
from ..BaseDAO import BaseDAO, require_transaction
from sqlalchemy import select


class reportsDAO(BaseDAO):
    model: Lost_report | Found_report
    @require_transaction
    async def get_all_reports(self, user: User) -> list[Found_report] | list[Lost_report]:
        query = select(self.model).where(self.model.user_id == user.id)
        
        result = await self._session.scalars(query)

        return list(result)


class Lost_reportDAO(reportsDAO):
    model = Lost_report

class Found_reportDAO(reportsDAO):
    model = Found_report
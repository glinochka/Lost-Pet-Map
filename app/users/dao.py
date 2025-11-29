from ..alembic.database import async_session_maker
from ..alembic.models import User
from ..BaseDAO import BaseDAO

from sqlalchemy import select

class UserDAO(BaseDAO):
    model = User
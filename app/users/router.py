from sqlalchemy import select
from fastapi import APIRouter
from logging import getLogger

from .schemas import NewUser, LoginUser
from .utils import get_password_hash, verify_password

from ..alembic.models import User
from ..alembic.database import async_session_maker

logger = getLogger(__name__)


router = APIRouter(prefix='/api/users')
@router.post("/registration")
async def user_registration(new_user: NewUser):
    async with async_session_maker() as session:
        comm = select(User).where(User.name == new_user.name)
        double_user = await session.scalar(comm)
        if double_user:
            logger.info(f'{new_user.name} уже есть в базе данных')
            return {"status": "user already exists"}
        
        dict_new_user = new_user.model_dump()
        dict_new_user['password'] = get_password_hash(dict_new_user['password'])

        session.add(User(**dict_new_user))
        await session.commit()
    logger.info(f'{new_user.name} был добавлен')
    return {"status": "success"}
    

@router.post("/login")
async def user_login(login_user: LoginUser):
    async with async_session_maker() as session:
        comm = select(User).where(User.name == login_user.name)
        user = await session.scalar(comm)

        if not user:
            logger.info(f'{login_user.name} отсутствует в базе данных')
            return {"status": "wrong user"}
        
        if not verify_password(login_user.password, user.password):
            logger.info(f'{login_user.name} выдан неверный пароль')
            return {"status": "wrong password"}
        
        logger.info(f'{login_user.name} вошел в систему') 

        return {"status": "success"}
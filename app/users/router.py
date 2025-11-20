from fastapi import APIRouter
from logging import getLogger

from .schemas import NewUser


import sys
from pathlib import Path
parent_dir = str(Path(__file__).resolve().parent.parent)
sys.path.append(f'{parent_dir}')


from models import User
from database import async_session_maker

logger = getLogger(__name__)


router = APIRouter(prefix='/api/users')
@router.post("/registration")
async def user_registration(new_user: NewUser):
    async with async_session_maker() as session:
        session.add(User(**new_user.model_dump()))
        await session.commit()
    logger.info(f'{new_user.name} был добавлен')
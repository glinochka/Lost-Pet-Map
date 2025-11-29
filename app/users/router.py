from sqlalchemy import select

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from logging import getLogger

from .schemas import NewUser, LoginUser
from .dao import UserDAO

from ..utils.security import get_password_hash, verify_password
from ..utils.JWT import create_access_token, get_user_from_access_token



logger = getLogger(__name__)

router = APIRouter(prefix='/api/users')

http_bearer = HTTPBearer()

@router.post("/registration")
async def user_registration(new_user: NewUser):
    double_user = await UserDAO.find_one_by_filter(name=new_user.name)

    if double_user:
        logger.info(f'{new_user.name} уже есть в базе данных')
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь уже существует"
        )
    
    dict_new_user = new_user.model_dump()
    dict_new_user['password'] = get_password_hash(dict_new_user['password'])

    user = await UserDAO.add(dict_new_user)
        
    logger.info(f'{new_user.name} был добавлен')
    
    return {
            'access_token': create_access_token({'user_id':str(user.id)}),
            'token_type': 'bearer'
        }

@router.post("/login")
async def user_login(login_user: LoginUser):
    user = await UserDAO.find_one_by_filter(name=login_user.name)

    if not user:
        logger.info(f'{login_user.name} отсутствует в базе данных')
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Пользователь не найден"
        )
    
    if not verify_password(login_user.password, user.password):
        logger.info(f'{login_user.name} выдан неверный пароль')
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный пароль"
        )
    
    logger.info(f'{login_user.name} вошел в систему') 

    return {
        'access_token': create_access_token({'user_id':str(user.id)}),
        'token_type': 'bearer'
    }


@router.post("/check")
async def jwt_check(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
    token = credentials.credentials
    user = await get_user_from_access_token(token)
    return {"your_id": user.id}

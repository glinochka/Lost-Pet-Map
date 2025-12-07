
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from logging import getLogger

from enum import Enum

from .schemas import Report, Patched_report
from .dao import Lost_reportDAO, Found_reportDAO

from ..users.dao import UserDAO
from ..utils.JWT import get_user_from_access_token
from ..utils.convert import convert_to_dict
from ..alembic.database import async_session_maker

logger = getLogger(__name__)

router = APIRouter(prefix='/api/reports')

http_bearer = HTTPBearer()

class ReportType(str, Enum):
    LOST = "lost_report"
    FOUND = "found_report"
def check_report_type(report_type: str) -> Lost_reportDAO | Found_reportDAO:
    try:
        type_ = ReportType(report_type)

        if type_ == ReportType.LOST:
            modelDAO = Lost_reportDAO
        else:
            modelDAO = Found_reportDAO
        return modelDAO
    
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid report type (available: 'lost_report', 'found_report')"
        )

@router.post("/add/{report_type}")
async def add_report(
    new_lost_report: Report,
    report_modelDAO: Lost_reportDAO | Found_reportDAO = Depends(check_report_type),
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
    ):
    token = credentials.credentials
    async with async_session_maker() as session:
        user_dao = UserDAO(session)
        rep_mod_dao = report_modelDAO(session)
        async with session.begin():
            user = await get_user_from_access_token(token, user_dao)

            new_lost_report_dict = new_lost_report.model_dump()
            new_lost_report_dict['photo_url'] = str(new_lost_report_dict['photo_url'])
            new_lost_report_dict['user_id'] = user.id

            await rep_mod_dao.add(new_lost_report_dict)

    return Response(status_code=status.HTTP_201_CREATED)

@router.get("/all/{report_type}")
async def get_reports(
    report_modelDAO: Lost_reportDAO | Found_reportDAO = Depends(check_report_type),
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
    ):
    token = credentials.credentials
    async with async_session_maker() as session:
        user_dao = UserDAO(session)
        rep_mod_dao = report_modelDAO(session)
        async with session.begin():
            user = await get_user_from_access_token(token, user_dao)
            reports = await rep_mod_dao.get_all_reports(user)

    reports_list = [convert_to_dict(report) for report in reports]
    return reports_list

@router.delete("/delete/{report_type}/{id_}")
async def delete_reports(
    id_: str,
    report_modelDAO: Lost_reportDAO | Found_reportDAO = Depends(check_report_type),
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
    ):
    token = credentials.credentials
    async with async_session_maker() as session:
        user_dao = UserDAO(session)
        rep_mod_dao: Lost_reportDAO | Found_reportDAO = report_modelDAO(session)
        async with session.begin():
            
            user = await get_user_from_access_token(token, user_dao)
            deleting_report = await rep_mod_dao.find_one_by_filter(id = int(id_), user_id = user.id)

            if not deleting_report:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Объект не найден или у пользователя нет доступа"
                )
            
            await rep_mod_dao.delete(deleting_report)

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.patch("/patch/{report_type}/{id_}")
async def patch_reports(
    id_: str,
    patched_report: Patched_report,
    report_modelDAO: Lost_reportDAO | Found_reportDAO = Depends(check_report_type),
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
    ):
    token = credentials.credentials
    async with async_session_maker() as session:
        user_dao = UserDAO(session)
        rep_mod_dao: Lost_reportDAO | Found_reportDAO = report_modelDAO(session)

        async with session.begin():
            user = await get_user_from_access_token(token, user_dao)

            patching_report = await rep_mod_dao.find_one_by_filter(id = int(id_), user_id = user.id)

            if not patching_report:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Объект не найден или у пользователя нет доступа"
                )
            
            rep_mod_dao.update(patching_report, patched_report.model_dump(exclude_unset=True))
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
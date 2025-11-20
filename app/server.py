from fastapi import FastAPI

from logger_config import setup_logger
setup_logger()

from fastapi.middleware.cors import CORSMiddleware
from users import router as users_router
from origins import origins
import uvicorn



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_methods = ['*'],
    allow_headers = ['*'],
    allow_credentials = True
)

app.include_router(users_router.router)



if __name__ == "__main__":

    uvicorn.run(
        "server:app",
        host="0.0.0.0",  # Доступно для всех в сети (сервер доступен по локальной сети)
        port=8000,
        reload=True  # Для разработки
    )
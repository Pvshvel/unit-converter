from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
import logging

from app.exceptions import BaseAppException
from app.routers import router as conversion_router


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI()


@app.exception_handler(BaseAppException)
async def app_exception_handler(request, exc):
    logger.error("Application error: %s", exc.message)
    return JSONResponse(status_code=exc.status_code, content={"error": exc.message})


app.include_router(conversion_router)


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, log_level='info')

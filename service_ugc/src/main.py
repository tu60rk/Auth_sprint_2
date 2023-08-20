import uvicorn
import logging

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.api.v1 import film_progress
from src.core.config import ugc_settings
from src.core.logger import LOGGING


app = FastAPI(
    title=ugc_settings.PROJECT_NAME,
    description=ugc_settings.PROJECT_DESCRIPTION,
    version=ugc_settings.API_VERSION,
    docs_url='/api/v1/openapi',
    openapi_url='/api/v1/openapi.json',
    default_response_class=ORJSONResponse,
    # root_path='/ugc',
)
app.include_router(film_progress.router, prefix='/api/v1/producer')

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=ugc_settings.UGC_APP_HOST,
        port=ugc_settings.UGC_APP_PORT,
        reload=True,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )

import logging
import os
from datetime import datetime
from typing import Dict

from fastapi import FastAPI
from pydantic import BaseModel
from starlette import status

from api.ecg.infrastructure.views.ecg import ecgs_router

logger = logging.getLogger(__name__)

os.environ["TZ"] = "UTC"

# create the api
api = FastAPI(
    title="ECG Service",
    version="1.0.0",
)

api.include_router(ecgs_router, tags=["ECGs"], prefix="/ecgs")


# health endpoint
class HealthOut(BaseModel):
    message: str
    version: str
    time: datetime

    class Config:
        schema_extra = dict(
            example=dict(
                message=f"{api.title} - OK",
                version=api.version,
                time=datetime.utcnow(),
            )
        )


@api.get(
    path="/health",
    tags=["Health"],
    description="Check the health of the API.",
    status_code=status.HTTP_200_OK,
    response_model=HealthOut,
)
def health() -> Dict:
    logger.info(f"GET Health")
    return dict(
        message=f"{api.title} - OK",
        version=api.version,
        time=datetime.utcnow(),
    )

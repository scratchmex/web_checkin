from fastapi import APIRouter

from .. import schemas

router = APIRouter()


@router.get("/", response_model=schemas.Message)
async def root():
    return {"message": "Hello there!. Inquiring?."}

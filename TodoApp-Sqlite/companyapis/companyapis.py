from fastapi import APIRouter, Depends
from . import dependencies

router = APIRouter(
    prefix="/companyapis",
    tags=["companyapis"],
    dependencies=[Depends(dependencies.get_token_header)],
    responses={
        404: {"detail": "Not Found"}
    }
)

@router.get("/")
async def get_company_name():
    return "COMPANYAPI"

@router.get("/employees")
async def number_of_employees():
    return 120
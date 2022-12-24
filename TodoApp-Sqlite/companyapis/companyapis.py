from fastapi import APIRouter


router = APIRouter(
    prefix="/companyapis",
    tags=["companyapis"],
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
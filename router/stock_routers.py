from fastapi import APIRouter, status
from service import stock_basic_service

router = APIRouter()

@router.post("/stock/basics/init", status_code = status.HTTP_201_CREATED)
def init_stock_basics():
    stock_basic_service.init_stock_basics()
    return {"result": "Success"}


@router.get("/stock/{symbol}", status_code = status.HTTP_200_OK)
def get_stock(symbol: str):
    return stock_basic_service.get_stock(symbol)
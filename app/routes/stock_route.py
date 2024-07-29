from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from http import HTTPStatus
from app.dtos.response_dtos import ResponseStocksDTO, ResponseStockDetailsDTO

from app.db.database import get_db
from app.db.crud import Crud
from app.controllers.brapi_stocks_controller import BrapiStocksController


router = APIRouter(prefix='/stock', tags=['stock'])

@router.get("", 
            status_code=HTTPStatus.OK,
            response_model=List[ResponseStocksDTO])
def get_stocks(db: Session = Depends(get_db)):
    return Crud(db).get_all_ative_stocks()

@router.get("/{ticker}/{time_range}",
            status_code=HTTPStatus.OK,
            response_model=ResponseStockDetailsDTO)
def get_stock_info(ticker: str, 
                   time_range: str):
    return BrapiStocksController().get_stock_info(ticker, time_range)
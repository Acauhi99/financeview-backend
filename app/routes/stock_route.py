from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.sql.database import get_db
from app.sql.crud import Crud
from app.controllers.BrapiStockController import BrapiStockController

router = APIRouter(prefix='/stock', tags=['stock'])

@router.get("")
def get_stocks(db: Session = Depends(get_db)):
    return Crud(db).get_all_ative_stocks()

@router.get("/{ticker}")
def get_stock_info(ticker: str):
    return BrapiStockController().get_stock_info(ticker)
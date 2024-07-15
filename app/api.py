from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers.BrazillianStocksController import BrazillianStocksController
from app.controllers.BrapiStockController import BrapiStockController

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/stocks", tags=["stocks"])
def get_stocks():
    return BrazillianStocksController().get_stocks()

@app.get("/stocks/{ticker}", tags=["stocks"])
def get_stock_info(ticker: str):
    return BrapiStockController().get_stock_info(ticker)
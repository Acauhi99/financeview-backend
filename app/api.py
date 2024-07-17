from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from apscheduler.schedulers.background import BackgroundScheduler
from app.controllers.BrapiStockController import BrapiStockController
from app.crons.ActiveStocksCronJob import ActiveStocksCronJob

from app.sql.database import get_db
from app.sql.crud import Crud

scheduler = BackgroundScheduler()

origins = [
    "http://localhost:3000",
    "localhost:3000",
]

scheduler.add_job(ActiveStocksCronJob.get_updated_stocks, 'interval', minutes=43200)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup")
    if not scheduler.running:
        scheduler.start()
    ActiveStocksCronJob.get_updated_stocks()
    yield
    print("Shutdown")
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/stocks", tags=["stocks"])
def get_stocks(db: Session = Depends(get_db)):
    return Crud(db).get_all_ative_stocks()

@app.get("/stocks/{ticker}", tags=["stocks"])
def get_stock_info(ticker: str):
    return BrapiStockController().get_stock_info(ticker)

@app.get("/healthcheck", tags=["healthcheck"])
async def health():
    return {"status": "ok"}
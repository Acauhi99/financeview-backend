from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.routes.stock_route import router as stock_router
from app.routes.user_route import router as user_router
from app.routes.test_route import router as test_router
from apscheduler.schedulers.background import BackgroundScheduler
from app.crons.active_stocks_cron_job import ActiveStocksCronJob

scheduler = BackgroundScheduler()

origins = [
    "https://localhost:3000",
    "http://localhost:3000",
    "https://localhost:8000",
    "http://localhost:8000",
    "https://localhost:80",
    "http://localhost:80",
    "https://financeview-frontoffice.vercel.app",
    "http://financeview-frontoffice.vercel.app"
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

@app.options("/{rest_of_path:path}")
def preflight_handler():
    return {}

@app.get("/")
def root():
    return {"message": "FinanceView API"}

app.include_router(stock_router)
app.include_router(user_router)
app.include_router(test_router)
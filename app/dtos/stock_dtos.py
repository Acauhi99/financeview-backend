from datetime import datetime
from typing import List
from pydantic import BaseModel

class HistoricalStockDataPriceDTO(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    adjustedClose: float

    class Config:
        arbitrary_types_allowed = True

class StockDataDTO(BaseModel):
    currency: str
    shortName: str
    longName: str
    regularMarketChange: float
    regularMarketChangePercent: float
    regularMarketTime: datetime 
    regularMarketPrice: float
    regularMarketDayHigh: float
    regularMarketDayRange: str
    regularMarketDayLow: float
    regularMarketVolume: int
    regularMarketPreviousClose: float
    regularMarketOpen: float
    fiftyTwoWeekRange: str
    fiftyTwoWeekLow: float
    fiftyTwoWeekHigh: float
    symbol: str
    usedInterval: str
    usedRange: str
    historicalDataPrice: List[HistoricalStockDataPriceDTO]
    validRanges: List[str]

    class Config:
        arbitrary_types_allowed = True

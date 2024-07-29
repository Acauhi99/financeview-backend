from typing import List, Optional
from pydantic import BaseModel

from app.dtos.feedback_dtos import FeedbackReadDTO
from app.dtos.stock_dtos import StockDataDTO

class ResponseMessageDTO(BaseModel):
    message: str

class ResponseUserTokenDTO(BaseModel):
    access_token: str
    token_type: str
    exp: str

class ResponseUserUrlImageDTO(BaseModel):
    url_image:Optional[str]

class ResponseUserFavoriteStocksDTO(BaseModel):
    favorites: List[str]

class ResponseFeedbackDTO(BaseModel):
    message: str
    data: List[FeedbackReadDTO]

class ResponseStocksDTO(BaseModel):
    id: int
    ticker: str

class ResponseStockDetailsDTO(BaseModel):
    results: List[StockDataDTO]

    class Config:
        arbitrary_types_allowed = True
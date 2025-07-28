"""
Схемы данных
"""

from datetime import datetime
from pydantic import BaseModel


class WalletInfoRequest(BaseModel):
    """
    Схема запроса к кошельку
    """

    wallet_address: str


class WalletInfoResponse(BaseModel):
    """
    Схема ответа от кошелька
    """

    wallet_address: str
    trx_balance: int
    bandwidth: int
    energy: int


class QueryHistory(BaseModel):
    """
    История запросов
    """

    id: int
    wallet_address: str
    trx_balance: int
    bandwidth: int
    energy: int
    created_at: datetime


class PaginatedQueryHistory(BaseModel):
    """
    Схема постраничной пагинации для навигации
    """

    items: list[QueryHistory]
    total: int
    page: int
    pages: int

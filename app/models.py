"""
Модели данных БД
"""

from sqlalchemy import Column, Integer, String, DateTime, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func


Base = declarative_base()


class WalletQuery(Base):
    """
    Очередь запросов в кошелек
    """

    __tablename__ = "wallet_queries"

    id = Column(Integer, primary_key=True, index=True)
    wallet_address = Column(String(34), index=True, nullable=False)
    trx_balance = Column(Numeric(precision=18, scale=6), nullable=False)
    bandwidth = Column(Integer, nullable=False)
    energy = Column(Integer, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )

"""
Взаимодействие с БД
"""

from sqlalchemy.orm import Session
import models


def create_wallet_query(db: Session, wallet_info: dict):
    """
    Создаем запись в кошелек
    """
    db_query = models.WalletQuery(
        wallet_address=wallet_info["wallet_address"],
        trx_balance=wallet_info["trx_balance"],
        bandwidth=wallet_info["bandwidth"],
        energy=wallet_info["energy"],
    )
    db.add(db_query)
    db.commit()
    db.refresh(db_query)
    return db_query


def get_query_history(db: Session, skip: int = 0, limit: int = 10):
    """
    Получаем историю по кошельку
    """
    total = db.query(models.WalletQuery).count()
    queries = db.query(models.WalletQuery).offset(skip).limit(limit).all()
    return {
        "items": queries,
        "total": total,
        "page": skip // limit + 1,
        "pages": (total + limit - 1) // limit,
    }

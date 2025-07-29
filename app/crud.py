"""
Взаимодействие с БД
"""

from typing import Any, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from . import models, schemas


def create_wallet_query(
    db: Session, wallet_info: schemas.WalletInfoResponse
) -> models.WalletQuery:
    """
    Создание записи в кошельке
    """
    db_query = models.WalletQuery(
        wallet_address=wallet_info.wallet_address,
        trx_balance=wallet_info.trx_balance,
        bandwidth=wallet_info.bandwidth,
        energy=wallet_info.energy,
    )
    db.add(db_query)
    db.commit()
    db.refresh(db_query)
    return db_query


def get_query_history(
    db: Session,
    wallet_address: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
) -> dict[str, Any]:
    """
    Получить историю кошелька
    """
    query = db.query(models.WalletQuery)
    if wallet_address:
        query = query.filter(models.WalletQuery.wallet_address == wallet_address)

    total = query.with_entities(func.count()).scalar()
    items = (
        query.order_by(models.WalletQuery.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    items = [schemas.QueryHistory.model_validate(item) for item in items]

    return {
        "items": items,
        "total": total,
        "page": skip // limit + 1 if limit else 1,
        "pages": (total + limit - 1) // limit if limit else 1,
    }

"""
Точка входа
"""

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models, schemas, tron
from .database import DatabaseManager

db_manager = DatabaseManager()

# вообще было бы лучше асинхронно все и оставила потенциально методы для того
# но так как в задании не указано, что нужно использовать асинхронный подход,
# то оставим синхронный подход для простоты и понятности + облегчение миграции
# а так лучше ассинхронно через алембик
models.Base.metadata.create_all(bind=db_manager.sync_engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/wallet-info/", response_model=schemas.WalletInfoResponse)
def get_wallet_info(
    wallet_request: schemas.WalletInfoRequest,
    db: Session = Depends(db_manager.get_session),
):
    """
    Получить данные по кошельку
    """
    wallet_info = tron.get_wallet_info_sync(wallet_request.wallet_address)
    if not wallet_info:
        raise HTTPException(status_code=404, detail="Wallet not found")

    crud.create_wallet_query(db, schemas.WalletInfoResponse(**wallet_info))

    return wallet_info


@app.get("/query-history/", response_model=schemas.PaginatedQueryHistory)
def get_query_history(
    page: int = 1, limit: int = 10, db: Session = Depends(db_manager.get_session)
):
    """
    Получить историю по кошельку
    """
    skip = (page - 1) * limit
    result = crud.get_query_history(db, skip=skip, limit=limit)
    return schemas.PaginatedQueryHistory(**result)

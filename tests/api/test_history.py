"""
Проверка записи в историю
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models, crud, schemas

# тут мокаю базу данных временной in-memory
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    models.Base.metadata.create_all(bind=engine)
    yield
    models.Base.metadata.drop_all(bind=engine)


def test_create_wallet_query():
    db = TestingSessionLocal()
    wallet_info = schemas.WalletInfoResponse(
        wallet_address="TTestAddress1234567890",
        trx_balance=123.456,
        bandwidth=789,
        energy=456,
    )
    obj = crud.create_wallet_query(db, wallet_info)
    assert obj.id is not None
    assert obj.wallet_address == wallet_info.wallet_address
    assert float(obj.trx_balance) == float(wallet_info.trx_balance)
    assert obj.bandwidth == wallet_info.bandwidth
    assert obj.energy == wallet_info.energy
    db.close()

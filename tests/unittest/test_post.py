"""
Проверка работы с post
"""
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

@pytest.fixture
def wallet_data():
    """
    Фикстура для обращения к кошельку
    """
    return {
        "wallet_address": "TTestAddress1234567890",
        "trx_balance": "123.456",
        "bandwidth": 789,
        "energy": 456
    }

def test_post_wallet_info(wallet_data):
    """
    Тест как работает запись в кошелек
    """
    with patch("app.tron.get_wallet_info_sync", return_value=wallet_data):
        response = client.post("/wallet-info/", json={"wallet_address": wallet_data["wallet_address"]})
        assert response.status_code == 200
        data = response.json()
        assert data["wallet_address"] == wallet_data["wallet_address"]
        # тут не преобразую Decimal в float из str во время сериализации чтобы 
        # не терять точность что в данном контексте важно
        assert data["trx_balance"] == wallet_data["trx_balance"]
        assert data["bandwidth"] == wallet_data["bandwidth"]
        assert data["energy"] == wallet_data["energy"]
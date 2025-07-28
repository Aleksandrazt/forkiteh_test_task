"""
Взаимодействие с трон
"""

import logging
import os

from tronpy import Tron
from tronpy.providers import HTTPProvider


class TronNetworkNotSetError(Exception):
    """
    Ошибка пустого пути к сети Tron
    """


def get_wallet_info_sync(wallet_address: str):
    """
    Получить данные по кошельку
    """
    tron_network = os.getenv("TRON_NETWORK")
    if not tron_network:
        logging.error("Не задана сеть tron в переменной окружения TRON_NETWORK")
        raise TronNetworkNotSetError(
            "Не задана сеть tron в переменной окружения TRON_NETWORK"
        )
    client = Tron(HTTPProvider(api_key=tron_network))

    try:
        account = client.get_account(wallet_address)
        if not account:
            return None

        balance = account.get("balance", 0) or 0
        bandwidth = account.get("free_net_usage", 0) or 0
        energy = account.get("account_resource", {}).get("energy_usage", 0) or 0

        return {
            "wallet_address": wallet_address,
            "trx_balance": balance,
            "bandwidth": bandwidth,
            "energy": energy,
        }
    except Exception as exp:
        logging.error("Проблема при подключении к сети Tron: %s", exp)
        raise exp

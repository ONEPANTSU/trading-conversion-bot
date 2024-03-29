import hashlib
import hmac
import time

import requests
from loguru import logger

from src.core.config.parsers.mexc_config import MEXCConfig
from src.services.parsers.abstract_parser import AbstractParser


class MexcParser(AbstractParser):
    def __init__(self, config: MEXCConfig):
        self.endpoint = "https://api.mexc.com/api/v3/rebate/affiliate/referral"
        self.api_key = config.api_key
        self.secret_key = config.secret_key

    def check_registration(self, uuid: str) -> bool:
        data = self.__get_affiliate_referral_data()
        if data:
            users = data["data"]["resultList"]
            for user in users:
                if user["uid"] == uuid:
                    return True
        return False

    def __get_affiliate_referral_data(self):
        timestamp = int(time.time() * 1000)
        params = {
            "timestamp": timestamp,
        }
        signature = self.__generate_signature(params)
        params["signature"] = signature

        headers = {
            "X-MEXC-APIKEY": self.api_key,
            "Content-Type": "application/json",
        }

        response = requests.get(self.endpoint, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            logger.error(
                f"Ошибка при выполнении запроса "
                f"({self.endpoint}): {response.status_code}"
            )
            return None

    def __generate_signature(self, params):
        total_params = "&".join(
            [f"{key}={params[key]}" for key in sorted(params.keys())]
        )
        signature = hmac.new(
            self.secret_key.encode("utf-8"),
            total_params.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return signature

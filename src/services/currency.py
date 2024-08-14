from datetime import datetime

import httpx
import requests
from fastapi import HTTPException

from src.error_messages.messages import ERROR_CURRENCY_RATE
from src.exceptions.custom_exceptions import CurrencyRateException


class Currency:
    base_url = "https://api.privatbank.ua/p24api"

    async def get_currency_rate(self, date: str, currency_value: str):
        get_url = f'{self.base_url}/exchange_rates?json&date={date}'

        try:
            response = requests.get(get_url)
            rates = response.json()["exchangeRate"]
            for rate in rates:
                if rate["currency"] == currency_value:
                    currency_rate = rate["saleRate"]
                    return currency_rate
        except (httpx.HTTPStatusError, httpx.RequestError, KeyError) as e:
            raise CurrencyRateException(ERROR_CURRENCY_RATE.format(details=str(e)))

    async def convert_currency(self, amount: float, date: str, currency_value: str):
        try:
            currency_rate = await self.get_currency_rate(date, currency_value)
            return round(amount / currency_rate, 2)
        except ValueError as e:
            raise CurrencyRateException(ERROR_CURRENCY_RATE.format(details=str(e)))

    async def set_currency_sum(self, spent_sum: float, date_value: datetime.date, currency_val: str) -> float:
        try:
            sum_in_currency = await self.convert_currency(spent_sum, date_value.strftime("%d.%m.%Y"),
                                                          currency_val)
            return sum_in_currency
        except CurrencyRateException as e:
            raise HTTPException(status_code=400, detail=ERROR_CURRENCY_RATE.format(details=str(e)))


currency_service = Currency()

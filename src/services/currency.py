import requests


class Currency:
    baseUrl = "https://api.privatbank.ua/p24api"

    async def get_currency_rate(self, date: str, currency_value: str = "USD"):
        get_url = f'/exchange_rates?json&date={date}'

        response = requests.get(self.baseUrl + get_url)
        rates = response.json()["exchangeRate"]
        for rate in rates:
            if rate["currency"] == currency_value:
                usd_rate = rate["saleRate"]
                return usd_rate


currency = Currency()

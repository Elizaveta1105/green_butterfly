import requests


class Currency:
    baseUrl = "https://api.privatbank.ua/p24api"

    async def get_currency_usd(self, date: str):
        get_url = f'/exchange_rates?json&date={date}'

        response = requests.get(self.baseUrl + get_url)
        rates = response.json()["exchangeRate"]
        for rate in rates:
            if rate["currency"] == "USD":
                usd_rate = rate["saleRate"]
                return usd_rate


currency = Currency()

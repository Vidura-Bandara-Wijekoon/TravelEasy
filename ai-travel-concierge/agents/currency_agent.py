import os
import requests

class CurrencyAgent:
    def get_currency_info(self, from_currency, to_currency, amount):
        api_key = os.getenv("EXCHANGERATE_API_KEY")
        if not api_key:
            return "Exchange rate API key is missing."
        try:
            url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{from_currency}/{to_currency}"
            response = requests.get(url)
            data = response.json()
            if data.get("result") != "success":
                return f"Failed to retrieve exchange rate: {data.get('error-type', 'Unknown error')}"
            rate = data["conversion_rate"]
            converted = float(amount) * rate
            return f"Exchange rate: 1 {from_currency} = {rate} {to_currency}. {amount} {from_currency} = {converted:.2f} {to_currency}."
        except Exception as e:
            return f"Error retrieving exchange rate: {str(e)}"
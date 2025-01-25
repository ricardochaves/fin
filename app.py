import requests
from flask import Flask
from flask_caching import Cache
import os
import finnhub

finnhub_client = finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY"))

# https://www.alphavantage.co/documentation/#currency-daily
ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

COIN_MARKETCAP_API_KEY = os.getenv("COIN_MARKETCAP_API_KEY")

app = Flask(__name__)
cache = Cache(config={'CACHE_TYPE': 'SimpleCache', "CACHE_DEFAULT_TIMEOUT": 3700})
cache.init_app(app)

@cache.cached()
def usd_brl():
    response = requests.get(f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=BRL&to_currency=USD&apikey={ALPHAVANTAGE_API_KEY}")
    value = float(response.json()["Realtime Currency Exchange Rate"]["8. Bid Price"])
    result = 1/value
    return round(result,2)

def crypto_quotes(symbol):
    response = requests.get(f"https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest?convert=USD&CMC_PRO_API_KEY={COIN_MARKETCAP_API_KEY}&id={symbol}")
    value = response.json()["data"][f"{symbol}"]["quote"]["USD"]["price"]
    return round(value,2)

@app.route("/healthcheck")
def healthcheck():
    return {"status": "ok"}

@app.route("/usd_brl")
def usd_brl_view():
    return {"USD_BRL": usd_brl()}
@app.route("/quotes")
def quotes():
    response = {
        "USD_BRL": usd_brl(),
        "ARGT": finnhub_client.quote('ARGT')["c"],
        "BAR": finnhub_client.quote("BAR")["c"],
        "CPER": finnhub_client.quote("CPER")["c"],
        "CORN": finnhub_client.quote("CORN")["c"],
        "QQQ" : finnhub_client.quote("QQQ")["c"],
        "MSOS": finnhub_client.quote("MSOS")["c"],
        "TFLO": finnhub_client.quote("TFLO")["c"],
        "BTC": crypto_quotes(1),
                }
    return response


if __name__ == "__main__":
    SERVER_HOST = os.environ.get('SERVER_HOST', "0.0.0.0")
    SERVER_PORT = int(os.environ.get('SERVER_PORT', 80))
    DEBUG = os.environ.get('DEBUG', False)
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=DEBUG)
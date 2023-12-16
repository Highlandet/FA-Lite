import requests
import json

from config import API_KEY

def get_crypto_rates():
    fiat = "RUB"
    responce = requests.get(f"https://rest.coinapi.io/v1/exchangerate/{fiat}?apikey-{API_KEY}",
             headers={"X-CoinAPI-Key":f"{API_KEY}"}
    )

    values = dict(json.loads(responce.text))
    rates = values['rates']
    currencies = [rate['asset_id_quote'] for rate in rates]

    btc_index = currencies.index('BTC')
    ton_index = currencies.index('TON')
    eth_index = currencies.index('ETH')
    usdt_index = currencies.index('USDT')
    bnb_index = currencies.index('BNB')

    btc_rate = round(1/rates[btc_index]['rate'], 2)
    ton_rate = round(1/rates[ton_index]['rate'], 2)
    eth_rate = round(1/rates[eth_index]['rate'], 2)
    usdt_rate = round(1/rates[usdt_index]['rate'], 2)
    bnb_rate = round(1/rates[bnb_index]['rate'], 2)
    return btc_rate, ton_rate, eth_rate, usdt_rate, bnb_rate

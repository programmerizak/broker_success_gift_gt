import requests
from django.conf import settings

def generate_address():
    api_key = settings.BLOCKCYPHER_API_KEY
    url = f"https://api.blockcypher.com/v1/btc/main/addrs?token={api_key}"
    response = requests.post(url)
    data = response.json()
    return data['address']

def check_balance(address):
    url = f"https://api.blockcypher.com/v1/btc/main/addrs/{address}/balance"
    response = requests.get(url)
    data = response.json()
    
    # Convert satoshis to BTC
    balance_btc = data['balance'] / 1e8  # 1 BTC = 100,000,000 Satoshis
    return balance_btc

from web3 import Web3
from django.conf import settings

def generate_ethereum_address():
    try:
        # Create a Web3 instance
        web3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{settings.INFURA_ETH_NETWORK}'))

        # Check connection (correct way)
        if not web3.is_connected():
            raise Exception("Web3 connection failed")

        # Create a new Ethereum account
        account = web3.eth.account.create()
        print(f"ETH Deposit Address, {account.address}")
        return account.address
    except Exception as e:
        print(f"Error generating Ethereum address: {e}")
        raise


# from web3 import Web3
# from django.conf import settings

# def generate_ethereum_address():
#     web3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{settings.INFURA_ETH_NETWORK}'))
#     account = web3.eth.account.create()
#     return account.address
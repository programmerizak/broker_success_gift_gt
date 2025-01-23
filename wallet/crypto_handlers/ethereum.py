from web3 import Web3
from django.conf import settings
from wallet.models import GeneratedWalletAddress

# Initialize Web3 instance
web3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{settings.INFURA_ETH_NETWORK}'))

########## USING LOCAL NETWORK(WORKING)
# Ensure web3 instance is correctly initialized
# web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# Function that generate eth wallet address(WORKING)
def generate_address():
    # Create a new Ethereum account
    account = web3.eth.account.create()
    # Save to database
    GeneratedWalletAddress.objects.create(
        wallet_provider='ETH',
        address=account.address,
        private_key=account.key.hex()
    )
    
    # Return the wallet address and private key
    # return account.address, account.key.hex()
    # Return the wallet address
    return account.address


def check_balance(address):
    # Get balance in Wei
    balance_wei = web3.eth.get_balance(address)
    # Convert balance to Ether
    balance_eth = web3.from_wei(balance_wei, 'ether')
    return balance_eth


def move_asset(private_key, destination_address, amount_eth):
    # Convert Ether amount to Wei (1 ETH = 10^18 Wei)
    amount_wei = web3.to_wei(amount_eth, 'ether')
    
    # Create account object from the private key
    account = web3.eth.account.from_key(private_key)
    
    # Get the current nonce for the account (number of transactions sent)
    nonce = web3.eth.get_transaction_count(account.address)
    
    # Build the transaction dictionary
    transaction = {
        'to': destination_address,
        'value': amount_wei,  # Amount to send in Wei
        'gas': 21000,  # Gas limit for a standard ETH transfer
        'gasPrice': web3.to_wei('50', 'gwei'),  # Gas price in Wei
        'nonce': nonce  # Nonce to prevent double spending
    }
    
    # Sign the transaction with the private key
    signed_tx = web3.eth.account.sign_transaction(transaction, private_key)
    
    # Send the signed transaction
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    
    # Return the transaction hash
    return web3.to_hex(tx_hash)


def estimate_gas_fee(destination_address, amount):
    # Get the current gas price from the network
    gas_price = web3.eth.gas_price
    
    # Set the gas limit for a typical ETH transfer
    gas_limit = 21000
    
    # Calculate the gas fee in Wei (gas price * gas limit)
    gas_fee = gas_price * gas_limit
    
    # Convert the gas fee from Wei to Ether and return
    return web3.from_wei(gas_fee, 'ether')


# def estimate_gas_fee(destination_address, amount):
#     gas_price = web3.eth.gas_price
#     gas_limit = 21000  # A typical transfer
#     gas_fee = gas_price * gas_limit
#     return web3.from_wei(gas_fee, 'ether')



## ### Function that generate eth wallet address(WORKING)
# def generate_address():
#     try:
#         # Create a new Ethereum account
#         account = web3.eth.account.create()

#         # Debugging information
#         wallet_address = account.address
#         print("WALLET ADDRESS:", wallet_address)
#         private_key = account.key.hex()
#         print("PRIVATE KEY:", private_key)

#         # Save to database
#         GeneratedWalletAddress.objects.create(
#             wallet_provider='ETH',
#             address=wallet_address,
#             private_key=private_key
#         )
        
#         # Return the wallet address and private key
#         # return wallet_address, private_key
    
#         # Return the wallet address
#         return wallet_address
#     except Exception as e:
#         # Print error message if any exception occurs
#         print(f"Error generating address: {str(e)}")
#         return None, None



# def move_asset(private_key, destination_address, amount):
#     account = web3.eth.account.privateKeyToAccount(private_key)
#     tx = {
#         'to': destination_address,
#         'value': web3.toWei(amount, 'ether'),
#         'gas': 21000,
#         'gasPrice': web3.toWei('50', 'gwei'),
#         'nonce': web3.eth.getTransactionCount(account.address),
#     }
#     signed_tx = account.signTransaction(tx)
#     tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
#     return tx_hash.hex()







#####################################################################



############################################################
############################################################
############################################################
############################################################


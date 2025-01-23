from web3 import Web3
from eth_account import Account
from web3.middleware import geth_poa_middleware
from eth_utils import to_checksum_address
from mnemonic import Mnemonic
import bip39,bip32,logging

logger = logging.getLogger(__name__)


###MY API KEY
infura_project_id = 'b386f4fab37c4f56bd36eddb6d7f6284'


class BlockchainService:

    def __init__(self, infura_project_id):
        """
        Initialize the BlockchainService with the provided Infura project ID.

        Args:
            infura_project_id (str): The Infura project ID.
        """
        # Connect to the Ethereum blockchain using Infura
        self.web3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{infura_project_id}'))
        # Add middleware for handling PoA (Proof of Authority) networks like Rinkeby
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # DONE
    def _private_key_to_address(self, private_key):
        """
        Derive the Ethereum address from the provided private key.

        Args:
            private_key (str): The private key of the wallet.

        Returns:
            str: The Ethereum address derived from the private key.
        """
        # Convert the private key to an Ethereum account
        account = Account.from_key(private_key)
        # Get the Ethereum address
        address = account.address
        return address

    # Done
    def connect_wallet(self, private_key):
        """
        Connect to the Ethereum blockchain using the provided private key.

        Args:
            private_key (str): The private key of the wallet to connect.

        Returns:
            str: The address of the connected wallet.
        """
        # Derive the Ethereum address from the private key
        wallet_address = self._private_key_to_address(private_key)
        return wallet_address

    ### DONE
    def _derive_private_key(self, mnemonic_phrase):
        """
        Derive the private key from the given mnemonic phrase.

        Args:
            mnemonic_phrase (str): The 12-word mnemonic phrase.

        Returns:
            str: The derived private key.
        """
        # Generate a seed from the mnemonic phrase
        seed = bip39.mnemonic_to_seed(mnemonic_phrase)
        # Derive the master private key from the seed
        master_key = bip32.MasterKey.from_seed(seed)
        # Derive the private key for the first account
        account_key = master_key.derive("m/44'/60'/0'/0/0")
        # Get the private key in hexadecimal format
        private_key_hex = account_key.private_key.to_hex()
        return private_key_hex

    ### DONE
    def _generate_mnemonic_phrase(self):
        """
        Generate a random 24-word mnemonic phrase.

        Returns:
            str: The generated mnemonic phrase.
        """
        m = Mnemonic("english")
        return m.generate(strength=128)

    ##### done
    def get_balance(self, wallet_address):
        """
        Get the balance of the given Ethereum wallet address.

        Args:
            wallet_address (str): The Ethereum wallet address to check.

        Returns:
            float: The balance of the wallet in Ether.
                   Returns None if there's an error or the address is invalid.
        """
        try:
            # Convert the wallet address to checksum format for consistency
            checksum_address = to_checksum_address(wallet_address)
            
            # Get the balance of the wallet in Wei (the smallest unit of Ether)
            balance_wei = self.web3.eth.getBalance(checksum_address)
            
            # Convert the balance from Wei to Ether
            balance_eth = self.web3.fromWei(balance_wei, 'ether')
            
            return balance_eth
        except Exception as e:
            # Log the error or handle it appropriately
            print(f"Error getting balance for address {wallet_address}: {e}")
            return None

    ## done
    def generate_wallet(self):
        """
        Generate a new Ethereum wallet address and private key.

        Returns:
            tuple: A tuple containing the wallet address and private key.
        """
        # Generate a new Ethereum account
        account = Account.create()
        # Extract the wallet address and private key
        wallet_address = account.address
        private_key = account.privateKey.hex()
        return wallet_address, private_key


    def send_transaction(self, sender_private_key, recipient_address, amount, gas):
        """
        Send a transaction from one wallet to another.

        Args:
            sender_private_key (str): The private key of the sender's wallet.
            recipient_address (str): The Ethereum address of the recipient.
            amount (float): The amount of Ether to send.
            gas (int): The gas limit for the transaction.

        Returns:
            str: The transaction hash.
        """
        sender_account = Account.from_key(sender_private_key)
        transaction = {
            'to': recipient_address,
            'value': self.web3.toWei(amount, 'ether'),
            'gas': gas,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(sender_account.address),
        }
        signed_txn = self.web3.eth.account.signTransaction(transaction, sender_private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return tx_hash.hex()

    def get_transaction_status(self, tx_hash):
        """
        Get the status of a transaction by its hash.

        Args:
            tx_hash (str): The transaction hash.

        Returns:
            dict: The transaction receipt.
        """
        return self.web3.eth.getTransactionReceipt(tx_hash)

    def interact_with_contract(self, contract_address, contract_abi, sender_private_key):
        """
        Interact with a smart contract deployed on the Ethereum blockchain.

        Args:
            contract_address (str): The address of the smart contract.
            contract_abi (list): The ABI (Application Binary Interface) of the smart contract.
            sender_private_key (str): The private key of the sender's wallet.

        Returns:
            str: The transaction hash.
        """
        contract = self.web3.eth.contract(address=contract_address, abi=contract_abi)
        sender_account = Account.from_key(sender_private_key)

        # Example: Call a read-only function of the smart contract
        contract.functions.getSomeValue().call()

        # Example: Send a transaction to a function of the smart contract
        txn_hash = contract.functions.someFunction().transact({'from': sender_account.address})

        return txn_hash


    def send_transaction(self, sender_private_key, recipient_address, amount):
        """
        Send an Ethereum transaction from the sender's address to the recipient's address.

        Args:
            sender_private_key (str): The private key of the sender's wallet.
            recipient_address (str): The Ethereum address of the recipient.
            amount (float): The amount of Ether to send in Ether.

        Returns:
            str: The transaction hash of the sent transaction.
        """
        # Convert the private key to an Ethereum account
        sender_account = Account.from_key(sender_private_key)
        sender_address = sender_account.address

        # Convert the recipient address to checksum format
        recipient_address = to_checksum_address(recipient_address)

        # Build the transaction
        transaction = {
            'to': recipient_address,
            'value': self.web3.toWei(amount, 'ether'),
            'gas': 21000,
            'gasPrice': self.web3.toWei('1', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(sender_address),
        }

        # Sign the transaction
        signed_tx = self.web3.eth.account.signTransaction(transaction, sender_private_key)

        # Send the transaction
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)

        return tx_hash.hex()

    def get_transaction_status(self, tx_hash):
        """
        Get the status of an Ethereum transaction.

        Args:
            tx_hash (str): The transaction hash of the transaction.

        Returns:
            str: The status of the transaction ('pending', 'success', 'failed').
        """
        receipt = self.web3.eth.getTransactionReceipt(tx_hash)
        if receipt is None:
            return 'pending'
        elif receipt['status'] == 1:
            return 'success'
        else:
            return 'failed'


    def send_transaction(self, sender_private_key, recipient_address, amount):
        try:
            # Convert private key to account object
            sender_account = self.web3.eth.account.privateKeyToAccount(sender_private_key)

            # Get nonce
            nonce = self.web3.eth.getTransactionCount(sender_account.address)

            # Build transaction object
            transaction = {
                'to': recipient_address,
                'value': self.web3.toWei(amount, 'ether'),  # Convert amount to Wei
                'gas': 2000000,  # Gas limit
                'gasPrice': self.web3.toWei('50', 'gwei'),  # Gas price in Gwei
                'nonce': nonce,
                'chainId': 1  # Ethereum mainnet chain ID
            }

            # Sign the transaction
            signed_transaction = sender_account.signTransaction(transaction)

            # Send the transaction
            tx_hash = self.web3.eth.sendRawTransaction(signed_transaction.rawTransaction)

            return tx_hash.hex()

        except Exception as e:
            logger.error("Error sending transaction: %s", e)
            return None


    def receive_transactions(self, wallet_address):
        try:
            # Get incoming transactions for the specified address
            transactions = self.web3.eth.get_transactions(wallet_address)

            # Process transactions if needed
            # For example, filter transactions related to the wallet_address

            return transactions

        except Exception as e:
            logger.error("Error receiving transactions: %s", e)
            return []


from .crypto_handlers import ethereum, bitcoin  # Import other handlers as needed

# Dictionary mapping currency symbols to their respective handlers
CRYPTO_HANDLERS = {
    'ETH': ethereum,
    'BTC': bitcoin,
    # Add other currency handlers here
}

# Function to generate a cryptocurrency address
def generate_crypto_address(currency_symbol):
    handler = CRYPTO_HANDLERS.get(currency_symbol)  # Retrieve the handler for the specified currency
    if handler:
        return handler.generate_address()  # Generate and return the address using the handler
    else:
        raise ValueError(f"No handler for currency {currency_symbol}")  # Raise an error if no handler is found

# Function to check the balance of a cryptocurrency address
def check_crypto_balance(currency_symbol, address):
    handler = CRYPTO_HANDLERS.get(currency_symbol)  # Retrieve the handler for the specified currency
    if handler:
        return handler.check_balance(address)  # Check and return the balance using the handler
    else:
        raise ValueError(f"No handler for currency {currency_symbol}")  # Raise an error if no handler is found


# Function to move cryptocurrency from one address to another
def move_crypto_asset(currency_symbol, private_key, destination_address, amount):
    handler = CRYPTO_HANDLERS.get(currency_symbol)  # Retrieve the handler for the specified currency
    if handler and hasattr(handler, 'move_asset'):
        return handler.move_asset(private_key, destination_address, amount)  # Move the asset using the handler
    else:
        raise ValueError(f"No handler for currency {currency_symbol}")  # Raise an error if no handler is found


def estimate_gas_fee(currency_symbol, destination_address, amount):
    # Retrieve the appropriate handler for the given cryptocurrency symbol
    handler = CRYPTO_HANDLERS.get(currency_symbol)
    
    # Check if the handler exists and has the 'estimate_gas_fee' function
    if handler and hasattr(handler, 'estimate_gas_fee'):
        # If the handler has the 'estimate_gas_fee' function, call it and return its result
        return handler.estimate_gas_fee(destination_address, amount)
    else:
        # If no handler exists for the given currency symbol, raise a ValueError
        raise ValueError(f"No handler for currency {currency_symbol}")

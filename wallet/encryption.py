from cryptography.fernet import Fernet
from django.conf import settings

# Ensure settings.ENCRYPTION_KEY is set to a 32-byte URL-safe base64-encoded key

def get_fernet():
    return Fernet(settings.ENCRYPTION_KEY)

def encrypt_data(data):
    fernet = get_fernet()
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data):
    fernet = get_fernet()
    return fernet.decrypt(encrypted_data.encode()).decode()

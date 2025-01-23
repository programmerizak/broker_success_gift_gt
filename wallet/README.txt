TO GENERATE
1. python manage.py shell
2. from cryptography.fernet import Fernet
3. ENCRYPTION_KEY = Fernet.generate_key().decode()
4. print(ENCRYPTION_KEY)
4. Store this in .env and reference in settings.py
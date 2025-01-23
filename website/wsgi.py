import os
# import sys

# sys.path.append("/var/www/bnba.io/venv/website/")
# sys.path.append("/var/www/bnba.io/venv/lib/python3.10/site-packages/")

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')

application = get_wsgi_application()

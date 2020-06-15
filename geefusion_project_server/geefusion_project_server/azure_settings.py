from .settings import *

STATICFILES_STORAGE = 'storages.backends.azure_storage.AzureStorage'
AZURE_ACCOUNT_NAME = os.getenv('AZ_STORAGE_ACCOUNT_NAME')
AZURE_CONTAINER = os.getenv('AZ_STORAGE_CONTAINER')
AZURE_ACCOUNT_KEY = os.getenv('AZ_STORAGE_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('APP_DB_NAME'),
        'USER': f'{os.getenv(POSTGRES_ADMIN_USER)}@{os.getenv('POSTGRES_SERVER_NAME')}',
        'PASSWORD': os.getenv('APP_DB_NAME'),
        'HOST': os.getenv('POSTGRESHOST'),
        'PORT': '5432',
        'OPTIONS': {'sslmode': 'require'},
    }
}
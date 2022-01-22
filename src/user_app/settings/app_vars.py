import os

from .base import BASE_DIR

# django vars
LANGUAGE_CODE = 'en-us'
TIME_ZONE = os.environ.get('TIME_ZONE', 'Asia/Dhaka')
USE_I18N = True
USE_L10N = True
USE_TZ = True
APPEND_SLASH = False
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

EMPLOYEE = "Employee"
MANAGER = "Manager"
CONSECUTIVE_WORKING_DAYS = int(os.environ.get('CONSECUTIVE_WORKING_DAYS', 3))
VOTING_LAST_HOUR = int(os.environ.get('VOTING_LAST_HOUR', 14))

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

if not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT, exist_ok=True)

# env
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = int(os.environ.get('DB_PORT'))

CELERY_BROKER_URL = "redis://redis:6379"
CELERY_RESULT_BACKEND = "redis://redis:6379"
# request setup
REQUEST_TIMEOUT = int(os.environ.get('REQUEST_TIMEOUT', 8))
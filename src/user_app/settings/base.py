import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

DEBUG = bool(int(os.environ.get('DEBUG', 0)))

SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = ['*']

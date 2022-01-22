from user_app.settings import DEBUG

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.DjangoModelPermissions',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'user_app.apis.renderers.DefaultRenderer',
    ),
    'DEFAULT_PAGINATION_CLASS': 'base.helpers.CustomPagination',
    'PAGE_SIZE': 10,
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler'
}

if not DEBUG:
    REST_FRAMEWORK['EXCEPTION_HANDLER'] = 'base.exceptions.custom_exception_handler'


CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_ALLOW_HEADER = [
    'username',
    'group',
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
CORS_ALLOW_HEADERS = '*'
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
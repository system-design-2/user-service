from rest_framework import exceptions, status
from rest_framework.views import Response, exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first to get the standard error response.
    response = exception_handler(exc, context)

    # if there is an IntegrityError and the error response hasn't already been generated
    if isinstance(exc, Exception) and not response:
        response = Response({'message': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response


class UnprocessableEntity(exceptions.APIException):
    status_code = 422
    default_detail = 'Cannot process with the data'
    default_code = 'unprocessable_entity'


class BadRequest(exceptions.APIException):
    status_code = 400
    default_detail = 'Bad Request'
    default_code = 'bad_request'

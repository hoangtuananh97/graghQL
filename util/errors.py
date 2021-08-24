from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class ErrorCreate(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Error Create.')
    default_code = 'ErrorCreate'


class ErrorUpdate(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Error Update.')
    default_code = 'ErrorUpdate'


class ErrorDelete(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Error Delete.')
    default_code = 'ErrorDelete'

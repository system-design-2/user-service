import logging

from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_condition import Or
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

from base.documentation import jwt_header
from base.permissions import IsManager
from restaurant.models import Restaurant
from restaurant.serializers import (RestaurantDetailsSerializer,
                                    RestaurantSerializer)

logger = logging.getLogger('user_app')


@method_decorator(name='list', decorator=swagger_auto_schema(manual_parameters=[jwt_header]))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(manual_parameters=[jwt_header]))
@method_decorator(name='create', decorator=swagger_auto_schema(manual_parameters=[jwt_header]))
class RestaurantViewSet(viewsets.ModelViewSet):
    """
    Creating restaurant
    """
    permission_classes = [Or(IsManager, IsAdminUser)]
    authentication_classes = [JWTAuthentication]
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'address']
    filter_fields = ['name', 'status']
    # lookup_field = 'name'
    http_method_names = ['get', 'post']

    def get_queryset(self):
        if IsManager.has_permission(self, request=self.request, view=self.get_view_name()):
            return super().get_queryset().filter(manager=self.request.user)
        return super().get_queryset()

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [Or(IsManager, IsAdminUser)]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RestaurantDetailsSerializer
        return RestaurantSerializer

import logging

from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_condition import Or
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

from base.documentation import jwt_header
from base.permissions import IsEmployee
from vote.models import Vote
from vote.serializers import VoteDetailsSerializer, VoteSerializer

logger = logging.getLogger('user_app')


@method_decorator(name='list', decorator=swagger_auto_schema(manual_parameters=[jwt_header]))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(manual_parameters=[jwt_header]))
@method_decorator(name='create', decorator=swagger_auto_schema(manual_parameters=[jwt_header]))
class VoteViewSet(viewsets.ModelViewSet):
    """
    Voting for restaurant menu
    """
    permission_classes = [IsEmployee]
    authentication_classes = [JWTAuthentication]
    queryset = Vote.objects.all().select_related('employee__user')
    serializer_class = VoteSerializer

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['employee__employee_id', 'employee__user__username']
    filter_fields = ['employee', 'menu', 'voting_date']
    http_method_names = ['get', 'post']

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [IsEmployee]
        else:
            permission_classes = [Or(IsAdminUser, IsEmployee)]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if IsAdminUser.has_permission(self, request=self.request, view=self.get_view_name()):
            return super().get_queryset()
        return super().get_queryset().filter(employee__user=self.request.user)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return VoteDetailsSerializer
        return VoteSerializer


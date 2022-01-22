import logging
from datetime import date

from django.db.models import Count
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import NotAcceptable
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from base.documentation import jwt_header
from vote.models import Result, Vote
from vote.serializers import ResultDetailsSerializer, ResultSerializer
from vote.utils import check_winner, get_previous_winner_restaurant_ids

logger = logging.getLogger('user_app')


@method_decorator(name='get', decorator=swagger_auto_schema(manual_parameters=[jwt_header]))
class ResultAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    """
    Getting results for the current day.
    """
    def get(self, request):
        # try:
        #     today_date = request.query_params.get('date', None)
        #     if not today_date:
        #         today_date = date.today()
        #     votes = Vote.objects.filter(menu__menu_date=today_date).\
        #         values('menu', 'menu__restaurant_id', 'menu__restaurant__name', 'menu__name', 'menu__menu_date').\
        #         annotate(number_of_vote=Count('menu')).order_by('-number_of_vote')
        #     if not votes:
        #         return Response({'message': f"No voting data found at {today_date}"})
        #     return Response(votes)
        # except Exception as e:
        #     logger.error(f"Error in {request.resolver_match.view_name}, error: {e}")
        #     return Response({'message': "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        today_date = request.query_params.get('date', None)
        if not today_date:
            today_date = date.today()
        votes = Vote.objects.filter(menu__menu_date=today_date).\
            values('menu', 'menu__restaurant_id', 'menu__restaurant__name', 'menu__name', 'menu__menu_date').\
            annotate(number_of_vote=Count('menu')).order_by('-number_of_vote')
        if not votes:
            return Response({'message': f"No voting data found at {today_date}", 'data': []})
        return Response(votes)


@method_decorator(name='post', decorator=swagger_auto_schema(manual_parameters=[jwt_header]))
class ResultPublishAPIView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    """
    Publish results for the current day. 
    The winner restaurant should not be the winner for 3 consecutive working days
    """
    def post(self, request):
        today_date = date.today()
        results = Result.objects.filter(publish_date=today_date)
        if results:
            result = results.last()
            serializer_context = {
                'request': request
            }
            serializer = ResultDetailsSerializer(result, context=serializer_context)
            response_data = {
                "message": "Result already published",
                "data": serializer.data,
            }
            return Response(response_data)
        votes = Vote.objects.filter(menu__menu_date=today_date).\
            values('menu', 'menu__restaurant_id', 'menu__restaurant__name', 'menu__name', 'menu__menu_date').\
            annotate(number_of_vote=Count('menu')).order_by('-number_of_vote')
        if not votes:
            return Response({'message': f"No voting data found at {today_date}", 'data': []})
        restaurant_ids = get_previous_winner_restaurant_ids()
        for vote in votes:
            winner = check_winner(restaurant_ids, vote['menu__restaurant_id'])
            if winner:
                break
        else:
            vote = votes.last()
        data = {
            'publish_date': vote['menu__menu_date'],
            'menu': vote['menu'],
            'number_of_votes': vote['number_of_vote'],
            'created_by': self.request.user.username,
            'updated_by': self.request.user.username
        }
        serializer = ResultSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        logger.info(f"Winning restaurant at {today_date} is {instance.menu.restaurant.name}")
        serializer_context = {
            'request': request
        }
        serializer_result = ResultDetailsSerializer(instance, context=serializer_context)
        return Response(serializer_result.data)
        # except NotAcceptable as e:
        #     logger.error(f"Error in {request.resolver_match.view_name}, error: {e}")
        #     return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        #
        # except Exception as e:
        #     logger.error(f"Error in {request.resolver_match.view_name}, error: {e}")
        #     return Response({'message': "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

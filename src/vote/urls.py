from django.urls import path
from rest_framework import routers

from vote.views import ResultAPIView, ResultPublishAPIView, VoteViewSet

app_name = 'vote'
router = routers.SimpleRouter()
router.register(r'', VoteViewSet, 'vote')

urlpatterns = [
    path('result/today/', ResultAPIView.as_view(), name='voting-result-today'),
    path('result/publish/', ResultPublishAPIView.as_view(), name='voting-result-publish'),
]
urlpatterns += router.urls

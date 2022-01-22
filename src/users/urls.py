from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.views import (ChangePasswordView, DeviceViewSet, LogoutView,
                         RegisterView, DeviceList)

router = routers.SimpleRouter()
router.register(r'device', DeviceViewSet, 'device')

app_name = 'users'
auth_urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth-register'),
    path('login/', TokenObtainPairView.as_view(), name='auth-login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('change-password/', ChangePasswordView.as_view(), name='auth-change-password'),
    path('logout/', LogoutView.as_view(), name='auth-logout'),
    path('device/list/<int:user_id>', DeviceList.as_view(), name='device-list-public-api'),
]

user_urlpatterns = router.urls

urlpatterns = auth_urlpatterns + user_urlpatterns

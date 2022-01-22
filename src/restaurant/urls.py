from django.urls import path
from rest_framework import routers

from restaurant.views import MenuList, MenuViewSet, RestaurantViewSet

app_name = 'restaurant'
router = routers.SimpleRouter()
router.register(r'menu', MenuViewSet, 'restaurant-menu')
router.register(r'', RestaurantViewSet, 'restaurant')

urlpatterns = [
    path('menu/today/', MenuList.as_view(), name='today-menu-list'),
]
urlpatterns += router.urls

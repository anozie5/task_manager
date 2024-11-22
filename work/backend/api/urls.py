from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

router=DefaultRouter()
router.register(r'task', JobView.as_view(), basename='task')
router.register(r'pay', PayView.as_view(), basename='pay')

urlpatterns=[
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', CreateUser.as_view(), name='signup'),
    path('login/', LoginUser.as_view(), name='login'),
    path('', include(router.urls)),
]
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from authentication.views import LogoutView, LoginAPIView


urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='authentication_login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='authentication_logout'),
]

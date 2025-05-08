from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CustomTokenObtainView, RegisterView, UserUpdateAPIView, GatUserDataView, CreateModeratorUser, \
    UpdateModeratorUser

urlpatterns = [
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token', CustomTokenObtainView.as_view(), name='custom_token_obtain'),
    path('api/register', RegisterView.as_view(), name='register'),
    path('api/getuser', GatUserDataView.as_view(), name='user-view'),
    path('api/create-moderator', CreateModeratorUser.as_view(), name='moderator-create'),
    path('api/update-moderator', UpdateModeratorUser.as_view(), name='moderator-update'),
    path('api/update/<str:username>', UserUpdateAPIView.as_view(), name='user-update'),  # username bo'yicha yangilash

]

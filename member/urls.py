from django.contrib import admin
from django.urls import path, include
from member.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('add-member/', Member.as_view()),
    # path('crud-team/', TeamsView.as_view()),
    path('member-team/', MemberTeamsView.as_view()),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', LoginView.as_view())

]

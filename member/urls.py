from django.contrib import admin
from django.urls import path, include
from member.views import *

urlpatterns = [
    path('add-member/', Member.as_view()),
    path('member-team/', MemberTeamsView.as_view()),
    path('login/', LoginView.as_view()),
    path('manager-teams/', TeamOfManagerView.as_view()),
    path('kudos-receptor/', MemberForKudosTransfer.as_view()),
    path('detail/', LoggedInUserDetail.as_view()),
    path('change-password/', ChangePassword.as_view())
]

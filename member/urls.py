from django.contrib import admin
from django.urls import path, include
from member.views import *

urlpatterns = [
    # path('crud-member/', Member.as_view()),
    # path('crud-team/', TeamsView.as_view()),
    path('member-team/', MemberTeamsView.as_view())

]

from django.contrib import admin
from django.urls import path
from kodus.views import *

urlpatterns = [
    path('kudos-transfer/', KudosTransfer.as_view()),
    path('daily-kudos/', AddDailyKudos.as_view()),
    path('current-kudos/', MemberKudosView.as_view()),
    path('kudos-transaction/', KudosTransaction.as_view()),
    path('teams/', TeamOfManagerView.as_view()),
    path('members-kudos/', ViewMemberKudosByManagerView.as_view()),
    # path('kudos/', KudosViewSet.as_view)
]
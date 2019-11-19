from django.contrib import admin
from django.urls import path
from kodus.views import *

urlpatterns = [
    path('kudos-transfer/', KudosTransfer.as_view()),
    path('daily-kudos/', AddDailyKudos.as_view()),
    path('current-kudos/', MemberKudosView.as_view()),
    path('kudos-transaction/', KudosTransaction.as_view()),
    path('members-kudos/', ViewMemberKudosByManagerView.as_view()),
    path('member-available-point/', MemberAvailablePointView.as_view()),
    path('dashboard-kudos-transaction/', DashboardKudosTransaction.as_view())
]
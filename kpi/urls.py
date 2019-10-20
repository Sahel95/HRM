from django.contrib import admin
from django.urls import path, include
from kpi.views import *

urlpatterns = [
    path('monthlydonated/', Createkpiformmonthly.as_view()),
    path('averagekpi/',MemberAverageKpi.as_view()),
    # path('member-team/', MemberTeam.as_view()),
    path('kpiformlist/', KpiFormList.as_view()),
    path('kpi-from/{id}/kpi-rate/', KpiRateShow.as_view()),
    path('kpi-form/{id}/kpi-monthly-rating/', KpiRatingShowForEmployee.as_view()),
    path('kpi-form/{id}/kpi-rating-member/', KpiRatingShowForManager.as_view())

]

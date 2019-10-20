from django.db import models
from  member.models import Members, Team
from django_enumfield import enum


class Status(enum.Enum):
    SENT_TO_EMPLOYEE = 0
    SEEN_BY_EMPLOYEE = 1
    SENT_TO_MANAGER = 2
    SEEN_BY_MANAGER = 3
    SUBMITTED_BY_MANAGER = 4


class KpiForm(models.Model):
    member = models.ForeignKey(Members, on_delete=models.CASCADE, related_name='kpiformmember')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='kpiformteam')
    submitted_by = models.ForeignKey(Members, on_delete=models.CASCADE , related_name='kpiformsubmittedby', null=True, blank=True)
    date = models.DateField()
    status = enum.EnumField(Status, default=Status.SEEN_BY_EMPLOYEE)
    avarage = models.IntegerField(null=True, blank=True)


class KpiRate(models.Model):
    kpi_form = models.ForeignKey(KpiForm, on_delete=models.CASCADE, related_name='rateform')
    value = models.CharField(max_length=30, null=True)
    key = models.IntegerField(null=True)
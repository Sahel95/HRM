from django.db import models
from django_enumfield import enum
from django.contrib.auth.models import AbstractUser, User
from datetime import date


class Position(enum.Enum):
    FRONTEND_DEVELOPER = 0
    BACKEND_DEVELOPER = 1
    PROJECT_MANAGER = 2
    DEVOPS = 3


class Rules(enum.Enum):
    EMPLOYEE = 0
    MANAGER = 1


class Members(User):
    national_code = models.IntegerField(null=True, blank=True)
    position = enum.EnumField(Position, default=Position.FRONTEND_DEVELOPER)
    tel = models.IntegerField(null=True, blank=True)
    kudos = models.IntegerField(default=0)
    available_point = models.IntegerField(default=0)
    kpi_rate = models.IntegerField(default=0)


class Team(models.Model):
    name = models.CharField(max_length=30)
    manager = models.ForeignKey(Members, on_delete=models.CASCADE)
    members = models.ManyToManyField(Members, related_name="memberteam", through="Membership")


class Membership(models.Model):
    member = models.ForeignKey(Members, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    role = enum.EnumField(Rules, default=Rules.EMPLOYEE)

    class Meta:
        unique_together = ('member', 'team',)

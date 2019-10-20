from django.db import models
from  member.models import Members
# Create your models here.


class Kudos (models.Model):
    from_member = models.ForeignKey(Members, on_delete=models.CASCADE, related_name='kudosfrom')
    to_member = models.ForeignKey(Members, on_delete=models.CASCADE, related_name='kudosto')
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    value = models.IntegerField()

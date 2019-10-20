from rest_framework import serializers
from member.models import *
from kpi.models import *


class MemberKudosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = ['id', 'kpi_rate']


class MemberTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = '__all__'


class KpiFormListSerializer(serializers.ModelSerializer):
    class Meta:
        model = KpiForm
        fields = '__all__'


class KpiRateShowSerializer(serializers.ModelSerializer):
    kpi_form = KpiFormListSerializer()

    class Meta:
        model = KpiRate
        fields = '__all__'




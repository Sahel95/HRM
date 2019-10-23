from rest_framework import serializers
from kodus.models import *
from member.models import *

from datetime import datetime


class KudosTransferSerializer (serializers.Serializer):
    to_member = serializers.IntegerField(min_value=1)
    value = serializers.IntegerField(min_value=1)

    def create(self, validated_data):
        to_member = Members.objects.get(id=validated_data['to_member'])
        k = Kudos(
            from_member=self.context['from_member'],
            to_member=to_member,
            value=validated_data['value']
            )
        k.save()
        to_member.kudos = to_member.kudos + validated_data['value']
        to_member.save()
        return k


class KudosTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kudos
        fields= '__all__'


class MemberKudosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = ['id', 'kudos']


class TeamOfManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class ViewMemberKudosByManagerSerializer(serializers.ModelSerializer):
    member = MemberKudosSerializer()

    class Meta:
        model = Membership
        fields = ['member']


from rest_framework import serializers

from member.models import *


class LoggedInUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = ['id', 'kudos', 'available_point', 'kpi_rate', 'first_name', 'last_name', 'position', '', 'national_code' , 'email', 'username']


class KudosReceptorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = ['id', 'first_name', 'last_name']


class MemberDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = ['id', 'first_name', 'last_name']


class ReadMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = "__all__"


class AddMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = ['national_code', 'first_name', 'last_name', 'mobile_number', 'position', 'username']

    def create(self, validated_data):
        m = Members(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            mobile_number=validated_data['mobile_number'],
            position=validated_data['position'],
            national_code=validated_data['national_code'],
            username=validated_data['username']
        )
        m.set_password(validated_data['national_code'])
        m.save()
        return m


class EditMemberDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = ['position', 'mobile_number', 'email', 'id']

    def update(self, instance, validated_data):
        instance.position = validated_data.get('position', instance.position)
        instance.mobile_number = validated_data.get('mobile_number', instance.mobile_number)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance


class ReadTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class CreateTeamSerializer(serializers.Serializer):
    manager_id = serializers.IntegerField()
    name = serializers.CharField()


    def create(self, validated_data):
        manager = Members.objects.get(id=validated_data['manager_id'])
        team = Team(
            name=validated_data['name'],
            manager=manager
        )
        team.save()
        return team


class MemberShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = '__all__'


class ChangePasswordSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    current_password = serializers.CharField(max_length=255)
    renter_password = serializers.CharField(max_length=255)
    new_password = serializers.CharField(max_length=255)

    def create(self, validated_data):
        self.context['member'].set_password(validated_data['new_password'])
        self.context['member'].save()
        return self.context['member']
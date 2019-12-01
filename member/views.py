from django.contrib.auth import authenticate
from django.core.paginator import Paginator
from django.http import QueryDict
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets


from django.contrib.auth.hashers import check_password
from .serializer import *
from .models import *

from itertools import chain

from rest_framework.authtoken.models import Token


class MembersCrudViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]

    queryset = Members.objects.all()
    serializer_class = ReadMemberSerializer


class TeamsCrudViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = ReadTeamSerializer
    # http_method_names = ['get', 'post', 'put']
    # def put(self, request):
    #     super()


class MemberShipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MemberShipSerializer
    # http_method_names = ['get', 'post', 'put']
    # def put(self, request):
    #     super()


class MemberTeamsView(APIView):
    def get(self, request):
        data = request.GET
        member = Members.objects.get(id=data['id'])
        membership = Membership.objects.filter(member=member)
        teams = QueryDict()
        for m in membership:
            team = Team.objects.filter(id=m.team.id)
            teams = list(chain(teams, team))
        serializer = ReadTeamSerializer(instance=teams, many=True)
        return Response(
            {
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if username is None or password is None:
            return Response(
                {
                    'error': 'Please provide both username and password'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        user = authenticate(username=username, password=password)
        if not user:
            return Response(
                {
                    'error': 'Invalid Credentials'
                },
                status=status.HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                'token': token.key
            },
            status=status.HTTP_200_OK
        )


class TeamOfManagerView(APIView):
    def get(self, request):
        manager = Members.objects.get(id=request.user.id)
        team = Team.objects.filter(manager=manager)
        serializer = ReadTeamSerializer(instance=team, many=True)
        return Response(
            {
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )


class Member(APIView):
    permission_classes = [AllowAny]

    #read member
    def get(self, request):
        members = Members.objects.all()
        serializer = ReadMemberSerializer(instance=members, many=True)
        return Response(
            {
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )

    # create member
    def post(self, request):
        data = request.data
        serializer = AddMemberSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'data': serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        else:
            return Response(
                {
                    'data': "serializer is NOT valid"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    # update member
    def put(self, request):
        data = request.data
        member = Members.objects.get(id=data['member_id'])
        serializer = EditMemberDataSerializer(instance=member, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'data': serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        else:
            return Response(
                {
                    'data': "serializer is NOT valid"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    # delete member
    def delete(self, request):
        data = request.data
        try:
            member = Members.objects.get(id=data['member_id'])
            member.delete()
            return Response(
                {
                    'msg': 'member deleted!'
                },
                status=status.HTTP_200_OK
            )
        except Members.DoesNotExist:
            return Response(
                {
                    'msg' : 'member does NOT exist!'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

class TeamsView(APIView):

    def get(self, request):
        teams = Team.objects.all()
        serializer = ReadTeamSerializer(instance=teams, many=True)
        return Response(
            {
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )

    def post(self, request):
        data = request.data
        serializer = CreateTeamSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'data': serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        else:
            return Response(
                {
                    'data': "serializer is NOT valid"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    def put(self, request):
        pass

    def delete(self, request):
        pass


class MemberForKudosTransfer(APIView):

    # read member
    def get(self, request):
        # logged_in_member=Members.objects.get(id=request.user.id)
        # members = Members.objects.all()
        member = Members.objects.get(id=request.user.id)
        members = Members.objects.exclude(id=request.user.id)
        serializer = KudosReceptorSerializer(instance=members, many=True)
        # for item in serializer.data:
        #     if item['id'] == member.id:
        #         print(item)
        #         print(len(serializer.data))
        #         del item
        #         print(len(serializer.data))

        return Response(
            {
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )


class LoggedInUserDetail(APIView):
    def get(self, request):
        member = Members.objects.get(id=request.user.id)
        serializer = LoggedInUserDetailSerializer(instance=member)
        return Response(
            {
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )


class ChangePassword(APIView):
    def post(self, request):
        data = request.data
        member = Members.objects.get(id=request.user.id)
        serializer = ChangePasswordSerializer(data=data, context={"member":member})
        if check_password(data['current_password'], request.user.password):
            if data['new_password'] == data['renter_password']:
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        {
                            'data':'password is changed!'
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {
                            'error': 'serializer is NOT valid!'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

            else:
                return Response(
                    {
                        'error': 'تکرار رمز عبور صحیح نیست !'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        else:
            return Response(
                {
                    'error': "رمز عبور فعلی صحیح نیست !"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

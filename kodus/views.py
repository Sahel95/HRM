from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny


from django.core.paginator import Paginator
from django.db.models import Q


from kodus.serializer import *
from member.models import *
from humanresource.settings import DAILY_MANAGER_KUDOS, DAILY_EMPLOYEE_KUDOS


class KudosTransfer(APIView):
    def post(self, request):
        from_member = Members.objects.get(id=request.user.id)
        serializer = KudosTransferSerializer(data=request.data, context={'from_member': from_member})
        if serializer.is_valid():
            u = Members.objects.get(id=request.user.id)
            x = int(float(request.data['value']))
            if u.available_point >= x:
                serializer.save()
                from_member.available_point = from_member.available_point - request.data['value']
                from_member.save()
                return Response(
                    {'message': 'Kudos Sent!',
                     # 'data': serializer.data
                     },
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {'message': 'You have NOT enough kudos'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        else:
            return Response(
                {'message': 'Serializer in NOT valid!'},
                status=status.HTTP_400_BAD_REQUEST
            )


class MemberKudosView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        member = Members.objects.get(id=request.user.id)
        serializer = MemberKudosSerializer(instance=member)
        return Response(
            {
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )


class KudosTransaction(APIView):
    def get(self, request):
        data = request.GET
        member = Members.objects.get(id=request.user.id)
        from_date = data.get('from_date', member.date_joined.date())
        to_date = data.get('to_date', date.today())
        kudos = Kudos.objects.filter(
            Q(to_member=member.id) | Q(from_member=member.id),
            date__range=[from_date, to_date]
        )
        serializer = KudosTransactionSerializer(instance=kudos, many=True)
        paginator = Paginator(serializer.data, 10)
        page = data['page']
        result = paginator.get_page(page)
        return Response(
            {
                'page': data['page'],
                'count': 10,
                'data': result.object_list
            },
            status=status.HTTP_200_OK
        )


class AddDailyKudos(APIView):
    def get(self, request):

        members = Members.objects.all()

        for m in members:
            member = Members.objects.get(id=m.id)
            role = Membership.objects.filter(member=member)
            for r in role:
                if r.role == 0:
                    member.available_point = member.available_point + DAILY_EMPLOYEE_KUDOS
                    member.save()
                elif r.role == 1:
                    member.available_point = member.available_point + DAILY_MANAGER_KUDOS
                    member.save()
        return Response(
            {'message': ' Kudos Donated! '},
            status=status.HTTP_200_OK
        )


class KudosViewSet(viewsets.ModelViewSet):
    queryset = Kudos.objects.all()
    serializer_class = KudosTransactionSerializer


class ViewMemberKudosByManagerView(APIView):
    def get(self, request):
        data = request.GET
        team = Team.objects.get(id=data['team_id'])
        members = Membership.objects.filter(team=team, role=0)
        serializer = ViewMemberKudosByManagerSerializer(instance=members, many=True)
        return Response(
            {
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )




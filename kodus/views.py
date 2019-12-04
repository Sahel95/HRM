from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny


from django.core.paginator import Paginator
from django.db.models import Q
from collections import OrderedDict


from kodus.serializer import *
from member.models import *
from humanresource.settings import DAILY_MANAGER_KUDOS, DAILY_EMPLOYEE_KUDOS


class KudosTransfer(APIView):
    def post(self, request):
        from_member = Members.objects.get(id=request.user.id)
        from_member_available_point = from_member.available_point - request.data['value']
        data = request.data
        to_member = Members.objects.get(id=data['to_member'])
        description = data.get('description', " ")
        if to_member.id == request.user.id:
            return Response(
                {'error': 'شما مجاز به ارسال کودس به خودتون نیستید!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            if data['value'] == 0:
                return Response(
                    {'error': 'حداقل سقف جابجایی 1 کودوس است !'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:

                serializer = KudosTransferSerializer(data=data, context={
                    'from_member': from_member,
                    'from_member_available_point': from_member_available_point,
                    'description': description

                })
                if serializer.is_valid():
                    u = Members.objects.get(id=request.user.id)
                    x = int(float(request.data['value']))

                    if u.available_point >= x:
                        serializer.save()
                        from_member.available_point = from_member_available_point
                        from_member.save()
                        return Response(
                            {'message': 'Kudos Sent!',
                             # 'data': serializer.data
                             },
                            status=status.HTTP_201_CREATED
                        )
                    else:
                        return Response(
                            {'error': 'موجودی شما کافی نیست !'},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                else:
                    return Response(
                        {'error': 'Serializer in NOT valid!'},
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


class MemberAvailablePointView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        member = Members.objects.get(id=request.user.id)
        serializer = MemberAvailablePointSerializer(instance=member)
        return Response(
            {
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )


class KudosTransaction(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = request.GET
        member = Members.objects.get(id=request.user.id)
        from_date = data.get('from_date', member.date_joined.date())
        to_date = data.get('to_date', date.today())
        if (from_date < to_date):
            kudos = Kudos.objects.filter(
                Q(to_member=member.id) | Q(from_member=member.id),
                date__range=[from_date, to_date]
            ).order_by('-date', '-time')
            serializer = KudosTransactionSerializer(instance=kudos, many=True)
            page_size = len(serializer.data) / 10
            for item in serializer.data:
                if item['to_member']['id'] == member.id:
                    item['from_member_available_point'] = ' '
                else:
                    item['to_member_kudos'] = ' '
            paginator = Paginator(serializer.data, 10)
            page = data['page']
            result = paginator.get_page(page)
            return Response(
                {
                    'page': data['page'],
                    'count': 10,
                    'page_size': page_size,
                    'data': result.object_list

                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'error': 'تاریخ وارد شده صحیح نمیباشد!'
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class AddDailyKudos(APIView):
    permission_classes = [AllowAny]

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

                # k = Kudos(
                #     from_member=Members.objects.get(id=1),
                #     to_member=m,
                #     value=DAILY_EMPLOYEE_KUDOS,
                #     from_member_available_point=" ",
                #     to_member_kudos=to_member_kudos
                # )

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


class DashboardKudosTransaction(APIView):
    def get(self, request):
        data = request.GET
        member = Members.objects.get(pk=request.user.id)
        kudos = Kudos.objects.filter(
            to_member=member.id
        ).order_by('-date', '-time')
        serializer = KudosTransactionSerializer(instance=kudos, many=True)
        for item in serializer.data:
            if item['to_member']['id'] == member.id:
                item['from_member_available_point'] = ' '
            else:
                item['to_member_kudos'] = ' '
        paginator = Paginator(serializer.data, 10)
        page = data['page']
        result = paginator.get_page(page)
        return Response(
            {
                'page': page,
                'count': 10,
                'data': result.object_list

            },
            status=status.HTTP_200_OK
        )

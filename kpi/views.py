from django.core.paginator import Paginator
from django.http import QueryDict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from itertools import chain

from kodus.serializer import *
from kpi.serializer import *
from member.models import *
from kpi.models import *


class Createkpiformmonthly(APIView):
    def post(self, request):
        members = Members.objects.all()
        for m in members:
            team = Membership.objects.filter(member=m)
            for t in team:
                member = Members.objects.get(id=m.id)
                team = Team.objects.get(id=t.id)
                kpi_form = KpiForm(
                    date=date.today(),
                    member=member,
                    status=0,
                    team=team
                )
                kpi_form.save()
                kpi_rate = KpiRate(
                    kpi_form=kpi_form
                )
                kpi_rate.save()

        return Response(
            {
                'message': 'KPI form Created!'
            },
            status=status.HTTP_201_CREATED
        )


# --------------------------------- gozareshgiri --------

class MemberAverageKpi(APIView):
    def get(self, request):
        data = request.GET
        member = Members.objects.get(id=data['id'])
        serializer = MemberKudosSerializer(instance=member)
        return Response(
            {
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )


# class MemberTeam(APIView):
#     def get(self, request):
#         data = request.GET
#         member = Members.objects.get(id=data['id'])
#         serializer = MemberTeamSerializer(instance=member)
#         return Response(
#             {
#                 'data': serializer.data
#             },
#             status=status.HTTP_200_OK
#         )


class KpiFormList(APIView):
    def get(self, request):
        data = request.GET
        member = Members.objects.get(id=data['id'])
        kpiform = KpiForm.objects.filter(member=member, status=4)
        serializer = KpiFormListSerializer(instance=kpiform, many=True)
        paginator = Paginator(serializer.data, 10)
        page = data['page']
        result = paginator.get_page(page)
        return Response(
            {
                'data': result.object_list
            },
            status=status.HTTP_200_OK
        )


class KpiRateShow(APIView):
    def get(self, request):
        data = request.GET
        kpi_form = KpiForm.objects.get(id=data['kpi_form_id'])
        kpi_rate = KpiRate.objects.filter(kpi_form=kpi_form)
        serializer = KpiRateShowSerializer(instance=kpi_rate, many=True)
        return Response(
            {
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )


class KpiRatingShowForEmployee(APIView):
    def get(self, request):
        data = request.GET
        member = Members.objects.get(id=data['id'])
        kpi_form = KpiForm.objects.get(member=member, status=0)
        kpi_rate = KpiRate.objects.filter(kpi_form=kpi_form)
        if kpi_rate:
            serializer = KpiRateShowSerializer(instance=kpi_rate, many=True)
            return Response(
                {
                    'data': serializer.data
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'data': 'This Page is NOT activate now!'
                },
                status=status.HTTP_404_NOT_FOUND
            )


class KpiRatingShowForManager(APIView):
    def get(self, request):
        data = request.GET
        member = Members.objects.get(id=data['id'])
        teams = Team.objects.filter(manager=member)
        result_list = QueryDict()
        for t in teams:
            members = t.members.all()
            for m in members:
                # kpi.models.KpiForm.DoesNotExist
                mem = Members.objects.get(id=m.id)
                tt = Team.objects.get(id=t.id)
                role = Membership.objects.get(member=mem, team=tt)
                if role.role == 0:
                    try:
                        kpi_form = KpiForm.objects.get(member=mem, status=2)
                        kpi_rate = KpiRate.objects.filter(kpi_form=kpi_form)
                        result_list = list(chain(kpi_rate, result_list))
                    except KpiForm.DoesNotExist:
                        pass

        serializer = KpiRateShowSerializer(instance=result_list, many=True)
        return Response(
            {
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )

from django.contrib.auth.models import Group
from  rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView

from .serialaizers import GroupSerialaizer



@api_view()
def hello_world_view(request: Request) -> Response:
    return Response({'msg': 'Hello world'})


class GroupsListView(ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerialaizer
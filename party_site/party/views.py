from .models import Party
from .serializers import PartyShortSerializer, PartyDetailSerializer

from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions


class PartyDetail(generics.RetrieveAPIView):
    serializer_class = PartyDetailSerializer
    queryset = Party.objects.all()


class PartyList(generics.ListAPIView):
    serializer_class = PartyShortSerializer
    queryset = Party.objects.all()


class PartyRegister(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PartyDetailSerializer
    queryset = Party.objects.all()

    def put(self, request, *args, **kwargs):
        party = self.get_object()
        party.members.add(request.user)
        return Response(self.serializer_class(instance=party, context={'request': request}).data)

    def delete(self, request, *args, **kwargs):
        party = self.get_object()
        party.members.remove(request.user)
        return Response(self.serializer_class(instance=party, context={'request': request}).data)

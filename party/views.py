from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Party
from .serializers import PartyDetailSerializer, PartyShortSerializer


class UserPermission(permissions.BasePermission):
    """
    Only authenticated users can register/unregister for party
    """

    def has_permission(self, request, view):
        if view.action in ('list', 'retrieve'):
            return True
        elif view.action in ('register', 'un_register'):
            return request.user.is_authenticated

        return False


class PartyViewSet(viewsets.ViewSet):
    permission_classes = (UserPermission,)

    def list(self, request):
        queryset = Party.objects.all()
        serializer_class = PartyShortSerializer(queryset, many=True, context={'request': request})
        return Response(serializer_class.data)

    def retrieve(self, request, pk=None):
        queryset = Party.objects.all()
        party = get_object_or_404(queryset, pk=pk)
        serializer = PartyDetailSerializer(party, context={'request': request})
        return Response(serializer.data)

    @action(methods=['put'], detail=True)
    def register(self, request, pk):
        """Register user to party"""
        queryset = Party.objects.all()
        party = get_object_or_404(queryset, pk=pk)

        party.members.add(request.user)
        return self.retrieve(request, pk)

    @register.mapping.delete
    def un_register(self, request, pk):
        """Remove user from party"""
        queryset = Party.objects.all()
        party = get_object_or_404(queryset, pk=pk)

        party.members.remove(request.user)
        return self.retrieve(request, pk)

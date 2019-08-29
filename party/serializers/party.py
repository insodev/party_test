from rest_framework import serializers

from ..models import Party
from .user import UserSerializer


class PartyShortSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Party
        fields = ('url', 'title', 'date', 'has_members')

        extra_kwargs = {
            'url': {'view_name': 'party-api:party-detail'},
        }


class PartyDetailSerializer(PartyShortSerializer):
    members = UserSerializer(many=True)

    class Meta(PartyShortSerializer.Meta):
        fields = PartyShortSerializer.Meta.fields + ('members', )

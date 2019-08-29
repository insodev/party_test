from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Party, User


class PartyTest(TestCase):
    def setUp(self):
        self.alice = User.objects.create(
            username='alice'
        )

        self.bob = User.objects.create(
            username='bob'
        )

        self.grey = User.objects.create(
            username='greyjoy'
        )

        self.alice_party = Party.objects.create(
            title='Alice Party',
            party_time_at=timezone.now(),
            party_time_till=timezone.now() + timezone.timedelta(hours=1),
            description='Alice Party all welcomed',
        )

        self.bob_party = Party.objects.create(
            title='Bob Party',
            party_time_at=timezone.now(),
            party_time_till=timezone.now() + timezone.timedelta(hours=1),
            description='Bob Party for Alice ',
        )

        self.grey_party = Party.objects.create(
            title='Grey Party',
            party_time_at=timezone.now(),
            party_time_till=timezone.now() + timezone.timedelta(hours=1),
            description='nobody comes',
        )

        self.alice_party.members.set([self.alice, self.bob, self.grey])
        self.bob_party.members.set([self.alice, self.bob])

        self.anonymous_client = APIClient()
        self.grey_client = APIClient()
        self.grey_client.force_authenticate(self.grey)

        self.url_party_list = reverse('party-api:party-list')
        self.url_grey_party = reverse('party-api:party-detail', kwargs={'pk': self.grey_party.pk})
        self.url_grey_party_register = reverse('party-api:party-register', kwargs={'pk': self.grey_party.pk})

    def test_users_count(self):
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(self.alice_party.members.count(), 3)
        self.assertEqual(self.bob_party.members.count(), 2)
        self.assertEqual(self.grey_party.members.count(), 0)

    def test_has_members(self):
        self.assertTrue(self.alice_party.has_members)
        self.assertFalse(self.grey_party.has_members)

    def test_connection(self):
        grey_response = self.grey_client.get(self.url_party_list)
        self.assertEqual(grey_response.status_code, status.HTTP_200_OK)
        response = self.client.get(self.url_party_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(grey_response.data, response.data)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 3)

    def test_register(self):
        self.assertFalse(self.grey_party.has_members)
        grey_response = self.grey_client.put(self.url_grey_party_register)
        self.assertEqual(grey_response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.grey_party.has_members, msg='{url} пользователь не добавлен'.format(
            url=self.url_grey_party_register
        ))
        self.grey_client.delete(self.url_grey_party_register)
        self.assertFalse(self.grey_party.has_members, msg='{url} пользователь {user} не удален'.format(
            url=self.url_grey_party_register,
            user=self.grey,
        ))
        response = self.client.put(self.url_grey_party_register)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

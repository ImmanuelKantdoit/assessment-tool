"""
Test for choices APIs
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Choice
from question.serializers import ChoiceSerializer


CHOICE_URL = reverse('question:choice-list')

def detail_url(choice_id):
    """Create and return a choice detail URL"""

    return reverse('question:choice-detail', args=[choice_id])


def create_choice(**params):
    """Create and return a sample choice"""
    defaults = {'choice': 'choice1'}
    defaults.update(params)

    return Choice.objects.create(**defaults)

def create_user(**params):
    """Create and return a new user"""

    return get_user_model().objects.create_user(**params)


class PublicQuestionAPITests(TestCase):
    """Test unauthenticated API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API"""
        res = self.client.get(CHOICE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateChoiceAPITests(TestCase):
    """Test Choices API"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='user@example.com',
            password='testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_create_choice(self):
        """Test creating a new choice"""
        # Create a sample question
        payload = {
        'choice': 'choice2',
        }

        # Use the created question in the payload
        res = self.client.post(CHOICE_URL, payload)

        # Ensure that the choice is created with the correct data
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_retrieve_choices(self):
        """Test retrieving a list of choices"""
        create_choice()
        create_choice()

        res = self.client.get(CHOICE_URL)

        choices = Choice.objects.all().order_by('-id')
        serializer = ChoiceSerializer(choices, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_choice_detail(self):
        """Test retrieving a choice detail"""
        choice = create_choice()
        url = detail_url(choice.id)
        res = self.client.get(url)

        serializer = ChoiceSerializer(choice)
        self.assertEqual(res.data, serializer.data)

    def test_update_choice(self):
        """Test updating a choice"""
        choice = create_choice()
        payload = {'choice': 'choice 2'}
        url = detail_url(choice.id)
        res = self.client.patch(url, payload)

        choice.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(choice.choice, payload['choice'])

    def test_deleting_choice(self):
        """Test deleting a choice"""
        choice = create_choice()

        url = detail_url(choice.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Choice.objects.filter(
                id=choice.id).exists()
            )

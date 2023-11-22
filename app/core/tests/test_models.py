"""
Tests for models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a new user"""
    return get_user_model().objects.create_user(email, password)


class ModelTest(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful"""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password, password)

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users"""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValuesError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_question(self):
        """Test creating a question"""
        question = models.Question.objects.create(
            question = "Is this a question?"
        )
        self.assertEqual(str(question), question.question)

    def test_create_choice(self):
        """Test creating a question with choices"""
        question = models.Question.objects.create(
            question="Is this a question?"
        )
        choice_list = ["Yes", "No", "Maybe"]

        # Create choices for the question
        models.Choice.save_choices(question, choice_list)

        # Retrieve the choices for the question using get_choices
        saved_choices = models.Choice.get_choices(question)

        # Check if the saved choices match the original choices
        self.assertEqual(saved_choices, choice_list)

    def test_create_answer(self):
        """Test creating a question"""
        question = models.Question.objects.create(
            question = "Is this a question?"
        )
        answer = models.Answer.objects.create(
            question=question,
            answer="No"
        )
        self.assertEqual(str(answer), answer.answer)








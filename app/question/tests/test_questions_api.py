"""
Test for Question APIs
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Question,
    Choice,
    )

from question.serializers import QuestionSerializer


QUESTION_URL = reverse('question:question-list')
CHOICE_URL = reverse('question:choice-list')


def detail_url(question_id):
    """Create and return a exam_question detail URL"""
    return reverse(
        'question:question-detail',
        args=[question_id]
        )


def create_choice(**params):
    """Create and return a sample choice"""
    defaults = {'choice': 'choice1'}
    defaults.update(params)

    return Choice.objects.create(**defaults)


def create_question(answer, **params):
    """Create and return a sample question"""
    defaults = {
        'question': 'sample question?',
        'answer': answer,
    }
    defaults.update(params)

    question = Question.objects.create(**defaults)
    return question


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class PublicQuestionAPITests(TestCase):
    """Test unauthenticated API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API"""
        res = self.client.get(QUESTION_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_examinee_cannot_retrieve_questions(self):
        """Test that examinee cannot retrieve a list of questions"""
        user = create_user(
            email='examinee@example.com',
            password='testpass123',
            role='examinee'
        )
        self.client.force_authenticate(user)

        res = self.client.get(QUESTION_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateQuestionAPIAPITests(TestCase):
    """Test authenticated API requests"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='user@example.com',
            password='testpass123',
            role='admin'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_questions(self):
        """Test retrieving a list of questions"""
        choice1 = create_choice()
        choice2 = create_choice()
        create_question(choice1)
        create_question(choice2)

        res = self.client.get(QUESTION_URL)

        questions = Question.objects.all().order_by('-id')
        serializer = QuestionSerializer(questions, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_question_detail(self):
        """Test get question"""
        choice = create_choice()
        question = create_question(choice)

        url = detail_url(question.id)
        res = self.client.get(url)

        serializer = QuestionSerializer(question)
        self.assertEqual(res.data, serializer.data)

    def test_partial_update_question(self):
        """Test partial update of a question"""
        question_sample = 'sample question'
        answer_choice = create_choice()
        exam_question = create_question(
            answer=answer_choice,
            question=question_sample,
        )
        payload = {'question': 'New question'}
        url = detail_url(exam_question.id)
        res = self.client.patch(url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        exam_question.refresh_from_db()

        # Ensure that the question is updated
        self.assertEqual(
            exam_question.question,
            payload['question']
            )

    def test_partial_update_answer(self):
        """Test partial update of a question"""
        original_answer = create_choice()
        exam_question = create_question(
            question='Sample question?',
            answer=original_answer
        )
        new_answer = create_choice(
            choice='new answer'
        )
        payload = {'answer': {'choice': new_answer.choice}}
        url = detail_url(exam_question.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Refresh the instance from the database
        exam_question.refresh_from_db()

        # Ensure that the answer is updated
        self.assertEqual(exam_question.answer.choice, new_answer.choice)

    def test_full_update(self):
        """Test full update of a question"""
        old_answer = create_choice()
        exam_question = create_question(
            question='Sample question',
            answer=old_answer
        )
        new_answer = create_choice(
            choice='new answer'
        )
        payload = {
            'question': 'Updated question',
            'answer': {'choice': new_answer.choice},
            'choices_data': [{'choice': 'Choice 1'}, {'choice': 'Choice 2'}]
        }
        url = detail_url(exam_question.id)
        res = self.client.put(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_question(self):
        """Test deleting a question successful"""
        answer = create_choice()
        question = create_question(answer)

        url = detail_url(question.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Question.objects.filter(
                id=question.id).exists()
            )

    def test_create_question_with_new_choices_and_answer(self):
        """Test creating a question with new choices"""
        payload = {
            'question': 'Sample question',
            'answer': {'choice': 'sample answer'},
            'choices': [
                {'choice': 'Choice A'},
                {'choice': 'sample answer'}
            ]
        }
        res = self.client.post(QUESTION_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        question_id = res.data.get('id')
        self.assertIsNotNone(question_id)

        question = Question.objects.get(id=question_id)
        self.assertEqual(question.choices.count(), 2)

        self.assertEqual(
            payload['answer']['choice'],
            question.choices.first().choice
        )

        # Loop through the choices in the payload
        for choice_data in payload['choices']:
            choice_exists = question.choices.filter(
                choice=choice_data['choice']
            ).exists()
            self.assertTrue(choice_exists)

    def test_create_question_with_existing_choices(self):
        """Test creating a question with existing choice"""
        payload = {
            'question': 'Sample question',
            'answer': {'choice': 'sample answer'},
            'choices': [
                {'choice': 'Answer A'},
                {'choice': 'sample answer'}
            ]
        }
        res = self.client.post(QUESTION_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        question = Question.objects.get(id=res.data['id'])

        # Create Choice instances and associate them with the question
        choice_data = [
            {'choice': 'Answer A'},
            {'choice': 'sample answer'}
        ]

        for choice in choice_data:
            Choice.objects.create(question=question, **choice)

        self.assertEqual(question.choices.count(), 2)

        for choice in payload['choices']:
            exists = question.choices.filter(
                choice=choice['choice'],
            ).exists()
            self.assertTrue(exists)

    def test_create_choice_on_update(self):
        """Test creating choice when updating a question"""
        answer = create_choice()
        question = create_question(answer)
        payload = {'choices': [
            {'choice': 'Yes'},
            {'choice': 'No'},
        ]}
        url = detail_url(question.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        choices = Choice.objects.filter(question=question)
        self.assertTrue(choices.exists())

    def test_update_question_assign_choice(self):
        """Test assigning an existing choice when updating a question"""
        # Create the initial choices and question
        choice1 = create_choice(choice='Choice 1')
        answer = create_choice()
        question = create_question(answer)
        question.choices.add(choice1)

        # Send a payload to update the question's choices
        payload = {'choices': [{'choice': 'Choice 2'}]}
        url = detail_url(question.id)
        res = self.client.patch(url, payload, format='json')

        # Refresh the question instance from the database
        question.refresh_from_db()

        # Check the response and the state of the question
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(question.choices.filter(choice="Choice 2").exists())
        self.assertFalse(question.choices.filter(choice="Choice 1").exists())

    def test_clear_question_choices(self):
        """Test clearing question choices"""
        choice = create_choice()
        question = create_question(choice)
        choices = Choice.objects.create(choice='Answer')
        question.choices.add(choices)

        payload = {'choices': []}
        url = detail_url(question.id)
        res = self.client.patch(url, payload, format='json')

        # Refresh the question instance from the database
        question.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(question.choices.count(), 0)

    def test_examinee_cannot_update_question(self):
        """Test that examinee cannot update a question"""
        examinee_user = create_user(
            email='examinee@example.com',
            password='testpass123',
            role='examinee'
        )
        self.client.force_authenticate(examinee_user)

        choice = create_choice()
        question = create_question(answer=choice)

        payload = {'question': 'Updated question'}
        url = detail_url(question.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        question.refresh_from_db()

        # Ensure that the question is not updated
        self.assertEqual(question.question, 'sample question?')

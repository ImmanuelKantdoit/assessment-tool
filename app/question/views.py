"""
Views for Question API
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from user.permissions import IsAdminUser

from core.models import (
    Question,
    Choice,
    )
from question import serializers


class QuestionViewSet(viewsets.ModelViewSet):
    """View for managing question APIs"""
    serializer_class = serializers.QuestionSerializer
    queryset = Question.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        """Retrieve choices"""
        return self.queryset.order_by('-id')


class ChoiceViewSet(viewsets.ModelViewSet):
    """View for managing choice APIs"""
    serializer_class = serializers.ChoiceSerializer
    queryset = Choice.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        """Retrieve choices"""
        return self.queryset.order_by('-id')

"""
URL mappings for the Question API
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from question import views


router = DefaultRouter()
router.register('question', views.QuestionViewSet)
router.register('choice', views.ChoiceViewSet)

app_name = 'question'

urlpatterns = [
    path('', include(router.urls)),
]

from rest_framework import serializers
from core.models import Question, Choice
from django.db import transaction


class ChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = ('id', 'choice')
        read_only_fields = ['id']


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, required=False)
    answer = ChoiceSerializer(required=True)

    class Meta:
        model = Question
        fields = ['id', 'question', 'answer', 'choices']
        read_only_fields = ['id']

    def _get_or_create_choices(self, choices, question):
        """Handle getting or creating choices as needed"""
        choice_objects = []

        # Clear existing choices
        question.choices.clear()

        for choice in choices:
            choice_obj, created = Choice.objects.get_or_create(
                choice=choice['choice'],
            )
            choice_objects.append(choice_obj)

        # Set the choices for the question
        question.choices.set(choice_objects)

        return choice_objects

    def create(self, validated_data):
        choices_data = validated_data.pop('choices', [])
        answer_data = validated_data.pop('answer')

        # Create question with answer
        answer_instance, _ = Choice.objects.get_or_create(**answer_data)
        question = Question.objects.create(answer=answer_instance, **validated_data)

        # Associate choices with the question
        self._get_or_create_choices(choices_data, question)

        return question

    def update(self, instance, validated_data):
        choices_data = validated_data.pop('choices', [])
        answer_data = validated_data.pop('answer', None)

        # Update or create choices
        choices = self._get_or_create_choices(choices_data, instance)

        # Update the question
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Update the answer if 'answer' is present in the validated data
        if answer_data:
            answer_instance, _ = Choice.objects.get_or_create(**answer_data)
            instance.answer = answer_instance
            instance.save()

        return instance




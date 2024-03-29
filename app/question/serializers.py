from rest_framework import serializers
from core.models import (
    Question,
    Choice
    )


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
        question = Question.objects.create(
            answer=answer_instance,
            **validated_data
            )

        # Associate choices with the question
        self._get_or_create_choices(choices_data, question)

        return question

    def update(self, instance, validated_data):
        instance.question = validated_data.get('question', instance.question)

        # Check if 'answer' is present in the validated data
        if 'answer' in validated_data:
            answer_data = validated_data.pop('answer')
            existing_answer_instance = instance.answer
            new_choice = answer_data.get('choice')

            # Check if there is an existing answer with the same choice
            if (
                existing_answer_instance
                and
                existing_answer_instance.choice == new_choice
            ):
                # Use the existing answer
                answer_instance = existing_answer_instance
            else:
                # Create a new answer
                answer_instance, _ = Choice.objects.get_or_create(
                    choice=new_choice
                    )
                instance.answer = answer_instance

        # Check if 'choices' is present in the validated data
        choices_data = validated_data.get('choices', [])
        if choices_data:
            self._get_or_create_choices(choices_data, instance)
        else:
            # If 'choices' is not present, clear existing choices
            instance.choices.clear()

        instance.save()
        return instance

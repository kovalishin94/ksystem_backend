from rest_framework import serializers

from .models import Test, Question, Option, Answer, TestResult


class TestCreatedByField(serializers.RelatedField):
    def to_representation(self, value):
        return {"id": value.profile.id, "first_name": value.profile.first_name, "last_name": value.profile.last_name}


class TestSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S", read_only=True)
    created_by = TestCreatedByField(read_only=True)

    class Meta:
        model = Test
        fields = [
            'id',
            'name',
            'created_by',
            'possible_attempts',
            'created_at',
            'updated_at'
        ]


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id',
            'body',
            'many_answers',
            'image',
            'test'
        ]


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = [
            'id',
            'body',
            'question',
            'is_true'
        ]


class OptionSolveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = [
            'id',
            'body',
            'question'
        ]


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'id',
            'option',
            'question',
            'user',
            'attempt'
        ]


class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = [
            'id',
            'user',
            'test',
            'attempt',
            'mark',
            'correct_answers',
            'wrong_answers',
            'created_at'
        ]

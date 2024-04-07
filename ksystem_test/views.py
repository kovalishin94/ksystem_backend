import json

from rest_framework import status
from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view, action, permission_classes

from security.permissions import IsAdmin, IsTestEditor, TestPermission, TestResultPermission

from .models import Test, Question, Option, Answer, TestResult
from .serializers import (TestSerializer,
                          QuestionSerializer,
                          OptionSerializer,
                          OptionSolveSerializer,
                          AnswerSerializer,
                          TestResultSerializer)


class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAdmin | IsTestEditor]

    @staticmethod
    def validate_test(test):
        questions = test.questions.all()
        if not questions:
            return False
        for question in questions:
            options = question.options.all()
            if options.count() <= 1:
                return False
            count_true = 0
            for option in options:
                if option.is_true:
                    count_true += 1
            if not count_true:
                return False
        return True

    def list(self, request):
        queryset = Question.objects.filter(test=request.GET.get('id'))
        options = Option.objects.filter(question__in=queryset)

        serializer = self.get_serializer(queryset, many=True)
        serializer_options = OptionSerializer(options, many=True)
        return Response({"questions": serializer.data, "options": serializer_options.data}, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        question = serializer.save()
        if question.many_answers:
            return

        options_in_question = question.options.all()

        if not options_in_question:
            return

        count_true = options_in_question.filter(is_true=True).count()

        if count_true == 1:
            return

        options_in_question[0].is_true = True
        options_in_question[0].save()

        if count_true:
            for opt in options_in_question[1:]:
                opt.is_true = False
                opt.save()

    @action(detail=False, methods=['get'], permission_classes=[])
    def solve_list(self, request):
        try:
            test = Test.objects.get(id=request.GET.get('id'))
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not self.validate_test(test):
            return Response({"test_valid": False}, status=status.HTTP_200_OK)

        count_results = TestResult.objects.filter(
            test=test, user=request.user).count()
        if test.possible_attempts <= count_results:
            return Response(status=status.HTTP_403_FORBIDDEN)

        queryset = Question.objects.filter(test=request.GET.get('id'))
        options = Option.objects.filter(question__in=queryset)

        serializer = self.get_serializer(queryset, many=True)
        serializer_options = OptionSolveSerializer(options, many=True)
        return Response({"questions": serializer.data, "options": serializer_options.data, "test_valid": True}, status=status.HTTP_200_OK)


class TestViewSet(ModelViewSet):
    queryset = Test.objects.select_related('created_by')
    serializer_class = TestSerializer
    permission_classes = [IsAdmin | TestPermission]

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        valid_list = []
        count_results = {}
        for test in queryset:
            count_results[str(test.id)] = TestResult.objects.filter(
                test=test, user=request.user).count()
            if QuestionViewSet.validate_test(test):
                valid_list.append(test.id)
        serializer = self.get_serializer(queryset, many=True)
        return Response({"tests": serializer.data, "count_results": count_results, "valid_list": valid_list})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        test = serializer.save()
        test.created_by = request.user
        test.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class OptionViewSet(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.UpdateModelMixin,
                    GenericViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    permission_classes = [IsAdmin | IsTestEditor]

    @staticmethod
    def validate_true_option(option):
        if option.question.many_answers:
            return
        options_in_question = option.question.options.exclude(id=option.id)

        if not options_in_question:
            if option.is_true:
                return
            option.is_true = True
            option.save()
            return

        if option.is_true:
            for opt in options_in_question:
                opt.is_true = False
                opt.save()

    def perform_create(self, serializer):
        option = serializer.save()
        self.validate_true_option(option)

    def perform_destroy(self, instance):
        if instance.question.many_answers or not instance.is_true:
            instance.delete()
            return

        options_in_question = instance.question.options.exclude(id=instance.id)

        if not options_in_question:
            instance.delete()
            return

        options_in_question[0].is_true = True
        options_in_question[0].save()
        instance.delete()

    def perform_update(self, serializer):
        option = serializer.save()
        self.validate_true_option(option)


class AnswerViewSet(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def create(self, request):
        # Проверка на наличие теста
        try:
            test = Test.objects.get(id=request.data.get('test'))
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Проверка на наличие имеющихся попыток
        count_results = TestResult.objects.filter(
            test=test, user=request.user).count()
        if test.possible_attempts <= count_results:
            return Response(status=status.HTTP_403_FORBIDDEN)

        # Проверка на наличие варианта ответа
        try:
            option = Option.objects.get(id=request.data.get("option"))
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Проверка на принадлежность варианта ответа и вопроса к тесту
        if option.question.test != test:
            return Response(status=status.HTTP_403_FORBIDDEN)

        # Получение существующих ответов, если вопрос может иметь только один ответ
        if not option.question.many_answers:
            answers = option.question.answers.filter(
                user=request.user, attempt=count_results + 1)
            # Удаление их при наличии
            if answers:
                for answer in answers:
                    answer.delete()

        # Валидация и создание ответа
        data = {
            "option": option.id,
            "question": option.question.id,
            "user": request.user.id,
            "attempt": count_results + 1
        }

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request):
        instance = self.get_object()
        try:
            is_admin = request.user.profile.permissions.filter(
                name='adm').exists()
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if not is_admin:
            return Response(status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        try:
            test = Test.objects.get(id=request.GET.get('test'))
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        count_results = TestResult.objects.filter(
            test=test, user=request.user).count()
        if test.possible_attempts <= count_results:
            return Response(status=status.HTTP_403_FORBIDDEN)

        questions = Question.objects.filter(test=test)

        queryset = Answer.objects.filter(
            question__in=questions, user=request.user, attempt=count_results + 1)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TestResultViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer
    permission_classes = [IsAdmin | TestResultPermission]

    def create(self, request):
        try:
            test = Test.objects.get(id=request.data.get("test"))
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        count_results = TestResult.objects.filter(
            user=request.user, test=test).count()
        if test.possible_attempts <= count_results:
            return Response(status=status.HTTP_403_FORBIDDEN)

        data = {"test": test.id, "user": request.user.id,
                "attempt": count_results + 1}
        questions = Question.objects.filter(test=test)
        answers = Answer.objects.filter(
            question__in=questions, attempt=data["attempt"], user=request.user).prefetch_related('option')

        question_ids = [question.id for question in questions]
        answer_ids = [answer.question.id for answer in answers]

        if not answer_ids:
            print('я тут 1')
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if set(question_ids) != set(answer_ids):
            print('я тут 2')
            return Response(status=status.HTTP_400_BAD_REQUEST)

        data["correct_answers"] = 0
        data["wrong_answers"] = 0

        for answer in answers:
            if answer.option.is_true:
                if answer.question.many_answers:
                    data["correct_answers"] += round(1 /
                                                     answer.question.options.filter(is_true=True).count(), 3)
                else:
                    data["correct_answers"] += 1
            else:
                data["wrong_answers"] += 1

        data["mark"] = round(data["correct_answers"] /
                             test.questions.count(), 3)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], permission_classes=[])
    def my_results(self, request):
        try:
            test = Test.objects.get(id=request.GET.get("id"))
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        test_results = TestResult.objects.filter(test=test, user=request.user)
        count_questions = test.questions.count()

        serializer = TestResultSerializer(test_results, many=True)

        return Response({"data": serializer.data, "count_questions": count_questions}, status=status.HTTP_200_OK)

from django.urls import path

from rest_framework import routers

from .views import TestViewSet, QuestionViewSet, OptionViewSet, AnswerViewSet, TestResultViewSet


router = routers.SimpleRouter()
router.register(r'results', TestResultViewSet, basename='result')
router.register(r'options', OptionViewSet, basename='option')
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'answers', AnswerViewSet, basename='answer')
router.register('', TestViewSet)

urlpatterns = router.urls

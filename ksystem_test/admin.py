from django.contrib import admin

from . import models


@admin.register(models.Test)
class AdminTest(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'created_by',
        'possible_attempts',
    )

    list_display_links = (
        'id',
        'name',
    )


@admin.register(models.Question)
class AdminQuestion(admin.ModelAdmin):
    list_display = (
        'id',
        'body',
        'many_answers',
        'test',
    )

    list_display_links = (
        'id',
        'body',
    )


@admin.register(models.Option)
class AdminOption(admin.ModelAdmin):
    list_display = (
        'id',
        'body',
        'question',
        'is_true',
    )

    list_display_links = (
        'id',
        'body',
    )


@admin.register(models.Answer)
class AdminAnswer(admin.ModelAdmin):
    list_display = (
        'id',
        'option',
        'question',
        'user',
        'attempt',
    )

    list_display_links = (
        'id',
    )


@admin.register(models.TestResult)
class AdminTestResult(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'test',
        'attempt',
        'mark',
    )

    list_display_links = (
        'id',
    )

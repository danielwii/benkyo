from django.contrib import admin

from . import models


class ChapterInline(admin.TabularInline):
    model = models.Chapter


@admin.register(models.Dictionary)
class DictionaryAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name', 'created_at', 'updated_at')
    inlines = [
        ChapterInline
    ]


class WordInline(admin.StackedInline):
    model = models.Word


@admin.register(models.Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'created_at', 'updated_at')
    list_filter = ('dictionary__name',)
    inlines = [
        WordInline
    ]

    def full_name(self, obj):
        return obj

    full_name.short_description = 'Chapter'
    full_name.admin_order_field = 'chapter__dictionary'


@admin.register(models.Word)
class WordAdmin(admin.ModelAdmin):
    pass

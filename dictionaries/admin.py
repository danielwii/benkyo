from django.contrib import admin
from django.utils.html import format_html

from core.utils import phonetic_wrapper
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
    class Media:
        css = {
            'all': ('admin/base.css',)
        }

    readonly_fields = ('phonetic_word',)

    def phonetic_word(self, obj):
        wrapper = '/'
        try:
            wrapper = phonetic_wrapper(obj.kana, obj.kanji, obj.marking)
        except Exception as e:
            print(e)
        print(wrapper)
        return format_html('<div class="phonetic-words">{}</div>', format_html(wrapper))

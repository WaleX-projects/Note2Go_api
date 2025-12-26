from django.contrib import admin
from .models import Note, Subject, Tag

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'subject', 'created_at')
    search_fields = ('title', 'ocr_text')
    list_filter = ('subject', 'created_at')


admin.site.register(Subject)
admin.site.register(Tag)

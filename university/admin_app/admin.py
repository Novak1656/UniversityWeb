from django.contrib import admin
from .models import StudyDirection, StudyDiscipline


@admin.register(StudyDirection)
class StudyDirectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'curator']
    list_display_links = ['id']


@admin.register(StudyDiscipline)
class StudyDisciplineAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['id']

from django.contrib import admin
from .models import Curator, StudyGroup, Student


@admin.register(Curator)
class CuratorAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'second_name', 'last_name', 'sex', 'old']
    list_display_links = ['id']


@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'direction', 'students_count']
    list_display_links = ['id']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'second_name', 'last_name', 'sex', 'group', 'year_of_admission']
    list_display_links = ['id']

from rest_framework import serializers
from .models import Student, StudyGroup, Curator


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        exclude = ['year_of_admission']


class StudyGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyGroup
        fields = '__all__'


class CuratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curator
        fields = '__all__'

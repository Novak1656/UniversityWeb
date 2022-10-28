from rest_framework import serializers
from .models import StudyDiscipline, StudyDirection


class StudyDisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyDiscipline
        fields = "__all__"


class StudyDirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyDirection
        fields = "__all__"

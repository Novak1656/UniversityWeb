from django.core.exceptions import ValidationError
from django.db.models import F
from rest_framework import serializers
from .models import Student, StudyGroup, Curator


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        exclude = ['year_of_admission']

    def __init__(self, *args, **kwargs):
        curator_pk = kwargs.pop('curator_pk')
        if curator_pk:
            groups = StudyGroup.objects.select_related('direction').filter(direction__curator__pk=curator_pk)
            self.fields['group'].queryset = groups
        super(StudentSerializer, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        obj = Student.objects.create(**validated_data)
        if obj.group.students_count == 20:
            raise ValidationError('Группа уже заполнена')
        obj.save()
        group = obj.group
        group.students_count = F('students_count') + 1
        group.save()
        obj.refresh_from_db()
        return obj

    def update(self, instance, validated_data):
        old_group = instance.group
        new_group = validated_data['group']

        if old_group != new_group:
            old_group.students_count = F('students_count') - 1
            old_group.save()
            old_group.refresh_from_db()

            new_group = validated_data['group']
            new_group.students_count = F('students_count') + 1
            new_group.save()
            new_group.refresh_from_db()
        return super(StudentSerializer, self).update(instance, validated_data)


class StudyGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyGroup
        exclude = ['students_count', 'direction']

    def create(self, validated_data):
        curator_pk = self.context['curator_pk']
        direction = Curator.objects.get(pk=curator_pk).direction
        group = StudyGroup.objects.create(direction=direction, **validated_data)
        group.save()
        return group


class CuratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curator
        fields = '__all__'

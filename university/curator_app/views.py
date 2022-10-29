from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Student, StudyGroup
from .serializers import StudentSerializer, StudyGroupSerializer


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.select_related('group').all()
    serializer_class = StudentSerializer

    def get_object(self):
        return get_object_or_404(Student, pk=self.kwargs.get('student_pk'))

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        kwargs['curator_pk'] = self.kwargs.get('curator_pk', None)
        return serializer_class(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        curator_pk = self.kwargs.get('curator_pk', None)
        if curator_pk:
            data = self.get_queryset().filter(group__direction__curator__pk=curator_pk)
            serialized_data = self.get_serializer(data,  many=True)
            return Response(serialized_data.data)
        return super(StudentViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        curator_pk = self.kwargs.get('curator_pk', None)
        student_pk = self.kwargs.get('student_pk', None)
        if curator_pk and student_pk:
            data = self.get_object()
            serialized_data = self.get_serializer(data, many=False)
            return Response(serialized_data.data)
        return super(StudentViewSet, self).retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        group = self.get_object().group
        group.students_count = F('students_count') - 1
        group.save()
        group.refresh_from_db()
        return super(StudentViewSet, self).destroy(request, *args, **kwargs)


class StudyGroupViewSet(ModelViewSet):
    queryset = StudyGroup.objects.select_related('direction').all()
    serializer_class = StudyGroupSerializer

    def get_serializer_context(self):
        context = super(StudyGroupViewSet, self).get_serializer_context()
        context['curator_pk'] = self.kwargs.get('curator_pk', None)
        return context

    def get_object(self):
        return get_object_or_404(StudyGroup, pk=self.kwargs.get('group_pk'))

    def list(self, request, *args, **kwargs):
        curator_pk = self.kwargs.get('curator_pk', None)
        if curator_pk:
            data = self.get_queryset().filter(direction__curator__pk=curator_pk)
            serializer_data = StudyGroupSerializer(data, many=True)
            return Response(serializer_data.data)
        return super(StudyGroupViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        curator_pk = self.kwargs.get('curator_pk', None)
        group_pk = self.kwargs.get('group_pk', None)
        if curator_pk and group_pk:
            data = self.get_object()
            serializer_data = StudyGroupSerializer(data, many=False)
            return Response(serializer_data.data)
        return super(StudyGroupViewSet, self).retrieve(request, *args, **kwargs)

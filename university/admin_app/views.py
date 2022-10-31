import os

from django.conf import settings
from django.http import HttpResponse
from django_celery_results.models import TaskResult
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import StudyDiscipline, StudyDirection
from curator_app.models import Curator
from .serializers import StudyDisciplineSerializer, StudyDirectionSerializer
from curator_app.serializers import CuratorSerializer
from .tasks import generate_report
from celery.result import AsyncResult


class StudyDisciplineViewSet(ModelViewSet):
    queryset = StudyDiscipline.objects.all()
    serializer_class = StudyDisciplineSerializer
    permission_classes = (IsAdminUser,)


class CuratorViewSet(ModelViewSet):
    queryset = Curator.objects.all()
    serializer_class = CuratorSerializer
    permission_classes = (IsAdminUser,)


class StudyDirectionViewSet(ModelViewSet):
    queryset = StudyDirection.objects.all()
    serializer_class = StudyDirectionSerializer
    permission_classes = (IsAdminUser,)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def start_generate_report(request):
    task = generate_report.delay()
    return Response({'message': 'Generation report has been started.', 'task_id': task.id}, status=202)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def show_generate_report_status(request, task_id):
    task = AsyncResult(task_id)
    return Response({'task': task_id, 'status': task.state}, status=200)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_report(request, task_id):
    task_result = TaskResult.objects.filter(task_id=task_id, status='SUCCESS').first().result
    filename = task_result.replace('"', '')
    with open(os.path.join(settings.BASE_DIR, filename), 'rb') as file:
        report = file.read()
    response = HttpResponse(report, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = "attachment; filename=UniversityReport.xlsx"
    return response

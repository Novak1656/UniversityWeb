import os

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django_celery_results.models import TaskResult
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import StudyDiscipline, StudyDirection
from curator_app.models import Curator
from .serializers import StudyDisciplineSerializer, StudyDirectionSerializer
from curator_app.serializers import CuratorSerializer
from .tasks import generate_report
from celery.result import AsyncResult

# Ограничить доступ только для админа и написать команду для создания суперюзера
class StudyDisciplineViewSet(ModelViewSet):
    queryset = StudyDiscipline.objects.all()
    serializer_class = StudyDisciplineSerializer


class CuratorViewSet(ModelViewSet):
    queryset = Curator.objects.all()
    serializer_class = CuratorSerializer


class StudyDirectionViewSet(ModelViewSet):
    queryset = StudyDirection.objects.all()
    serializer_class = StudyDirectionSerializer


@api_view(['GET'])
def start_generate_report(request):
    task = generate_report.delay()
    return Response({'message': 'Generation report has been started.', 'task_id': task.id}, status=202)


@api_view(['GET'])
def show_generate_report_status(request, task_id):
    task = AsyncResult(task_id)
    return JsonResponse({'task': task_id, 'status': task.state}, status=200)


@api_view(['GET'])
def get_report(request, task_id):
    task_result = TaskResult.objects.filter(task_id=task_id, status='SUCCESS').first().result
    filename = task_result.replace('"', '')
    with open(os.path.join(settings.BASE_DIR, filename), 'rb') as file:
        report = file.read()
    response = HttpResponse(report, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = "attachment; filename=UniversityReport.xlsx"
    return response

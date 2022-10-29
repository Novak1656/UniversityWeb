from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import StudyDiscipline, StudyDirection
from curator_app.models import Curator
from .serializers import StudyDisciplineSerializer, StudyDirectionSerializer
from curator_app.serializers import CuratorSerializer
from .tasks import generate_report

# Ограничить доступ только для админа
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

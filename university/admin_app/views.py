from rest_framework.viewsets import ModelViewSet
from .models import StudyDiscipline, StudyDirection
from curator_app.models import Curator
from .serializers import StudyDisciplineSerializer, StudyDirectionSerializer
from curator_app.serializers import CuratorSerializer


class StudyDisciplineViewSet(ModelViewSet):
    queryset = StudyDiscipline.objects.all()
    serializer_class = StudyDisciplineSerializer


class CuratorViewSet(ModelViewSet):
    queryset = Curator.objects.all()
    serializer_class = CuratorSerializer


class StudyDirectionViewSet(ModelViewSet):
    queryset = StudyDirection.objects.all()
    serializer_class = StudyDirectionSerializer

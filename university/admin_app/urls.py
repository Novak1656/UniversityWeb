from django.urls import path, include
from .views import StudyDisciplineViewSet, StudyDirectionViewSet, CuratorViewSet, start_generate_report
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'disciplines', StudyDisciplineViewSet)
router.register(r'curators', CuratorViewSet)
router.register(r'directions', StudyDirectionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('generate_report/', start_generate_report)
]

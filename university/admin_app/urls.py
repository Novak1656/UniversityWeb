from django.urls import path
from .views import StudyDisciplineViewSet, StudyDirectionViewSet, CuratorViewSet

urlpatterns = [
    path('disciplines/', StudyDisciplineViewSet.as_view(actions={'get': 'list', 'post': 'create'})),
    path('disciplines/<int:pk>/',
         StudyDisciplineViewSet.as_view(actions={'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})
         ),

    path('curators/', CuratorViewSet.as_view(actions={'get': 'list', 'post': 'create'})),
    path('curators/<int:pk>/',
         CuratorViewSet.as_view(actions={'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})
         ),

    path('directions/', StudyDirectionViewSet.as_view(actions={'get': 'list', 'post': 'create'})),
    path('directions/<int:pk>/',
         StudyDirectionViewSet.as_view(actions={'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})
         ),
]

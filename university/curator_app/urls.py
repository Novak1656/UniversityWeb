from django.urls import path
from .views import StudentViewSet, StudyGroupViewSet

urlpatterns = [
    path('<int:curator_pk>/students/', StudentViewSet.as_view(actions={'get': 'list', 'post': 'create'})),
    path('<int:curator_pk>/students/<int:student_pk>/',
         StudentViewSet.as_view(actions={'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})
         ),

    path('students/', StudentViewSet.as_view(actions={'get': 'list', 'post': 'create'})),
    path('students/<int:student_pk>/',
         StudentViewSet.as_view(actions={'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})
         ),

    path('<int:curator_pk>/groups/', StudyGroupViewSet.as_view(actions={'get': 'list', 'post': 'create'})),
    path('<int:curator_pk>/groups/<int:group_pk>/',
         StudentViewSet.as_view(actions={'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})
         ),

    path('groups/', StudyGroupViewSet.as_view(actions={'get': 'list', 'post': 'create'})),
    path('groups/<int:group_pk>/',
         StudentViewSet.as_view(actions={'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})
         ),
]

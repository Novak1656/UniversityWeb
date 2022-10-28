from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('university/admin/', include('admin_app.urls')),
    path('university/curator/', include('curator_app.urls')),
]

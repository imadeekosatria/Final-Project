from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('', views.file_upload, name='file_upload'),
    path('upload', views.file_upload, name='file_upload'),
    # path('upload_manual', views.file_upload, name='file_upload'),
    path('overview/<str:name>', views.overview, name='overview'),
    path('pso_process/', views.pso_process, name='pso_process'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
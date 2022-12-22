from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib import admin


urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    # path('', views.file_upload, name='file_upload'),
    path('upload', views.file_upload, name='file_upload'),
    path('upload_manual', views.manual, name='manual'),
    path('overview/<str:name>', views.overview, name='overview'),
    path('pso_process/', views.pso_process, name='pso_process'),
    path('comparison', views.comparison, name='comparison'),
    path('get_result_json/<int:id>', views.get_result_json, name='get_result_json'),
    path('resultTesting/<str:judul>/<int:id>', views.resultTesting, name='resultTesting'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
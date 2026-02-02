from django.urls import path
from . import views

app_name = 'my_app'

urlpatterns = [
    path('upload/', views.UploadFileView, name='upload_file'),
    path('process/', views.ProcessDataView, name='process_data')
]
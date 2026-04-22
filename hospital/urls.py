from django.urls import path
from . import views

urlpatterns = [
    path('', views.add_patient, name='add_patient'),
    path('queue/', views.queue_list, name='queue_list'),
    path('history/', views.queue_history, name='queue_history'),
    path('beds/', views.bed_dashboard, name='bed_dashboard'),
    path('assign-bed/<int:queue_id>/', views.assign_bed, name='assign_bed'),
    path('complete-patient/<int:queue_id>/', views.complete_patient, name='complete_patient'),
]
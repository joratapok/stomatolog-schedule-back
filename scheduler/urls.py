from django.urls import path
from scheduler import views

urlpatterns = [
    path('', views.ClinicListApiView.as_view()),
    path('create/', views.EventCreateApiView.as_view()),
    path('<int:pk>/', views.EventRetrieveUpdateDestroyAPIView.as_view()),

]

from django.urls import path
from scheduler import views

urlpatterns = [
    path('', views.EventListApiView.as_view()),

    path('create/', views.EventCreateApiView.as_view()),
    path('<int:pk>/', views.EventRetrieveUpdateDestroyAPIView.as_view()),

    path('cabinet/create/', views.CabinetCreateApiView.as_view()),
    path('cabinet/<int:pk>/', views.CabinetRetrieveUpdateDestroyAPIView.as_view()),

    path('customer/', views.CustomerListApiView.as_view()),
]

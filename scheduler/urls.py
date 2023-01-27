from django.urls import path
from scheduler import views

urlpatterns = [
    path('', views.EventListApiView.as_view()),

    path('create/', views.EventCreateApiView.as_view()),
    path('<int:pk>/', views.EventRetrieveUpdateDestroyAPIView.as_view(), name='event_update'),

    path('cabinet/create/', views.CabinetCreateApiView.as_view()),
    path('cabinet/<int:pk>/', views.CabinetRetrieveUpdateDestroyAPIView.as_view()),

    path('customer/', views.CustomerListApiView.as_view()),
    path('customer/<int:pk>/', views.CustomerRetrieveUpdateDestroyAPIView.as_view()),
    path('customer/<int:pk>/detail/', views.CustomerDetailRetrieveAPIView.as_view()),

    path('duty-shift/', views.DutyShiftListCreateApiView.as_view()),
    path('duty-shift/<int:pk>/', views.DutyShiftRetrieveUpdateDestroyAPIView.as_view()),

]

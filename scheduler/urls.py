from django.urls import path
from scheduler import views

urlpatterns = [
    path('', views.ClinicListApiView.as_view()),

    path('create/', views.EventCreateApiView.as_view()),
    path('<int:pk>/', views.EventRetrieveUpdateDestroyAPIView.as_view(), name='event_update'),
    path('<int:pk>/pdf/', views.get_invoice_of_payment, name='get_pdf'),

    path('cabinet/create/', views.CabinetCreateApiView.as_view()),
    path('cabinet/<int:pk>/', views.CabinetRetrieveUpdateDestroyAPIView.as_view()),

    path('customer/', views.CustomerListApiView.as_view()),
    path('customer/<int:pk>/', views.CustomerRetrieveUpdateDestroyAPIView.as_view()),
    path('customer/<int:pk>/detail/', views.CustomerDetailRetrieveAPIView.as_view()),

    path('duty-shift/', views.DutyShiftListCreateApiView.as_view()),
    path('duty-shift/<int:pk>/', views.DutyShiftRetrieveUpdateDestroyAPIView.as_view()),

]

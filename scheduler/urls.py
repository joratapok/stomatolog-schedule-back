from django.urls import path, include
from . import views

urlpatterns = [
    # # Вход
    # path('/api/auth/sign_in/', views.LoginUser.as_view(), name='login'),
    # # Авторизация
    # path('api/auth/sign_up/', views.create_employee, name='create_user'),
    # path('api/auth/', include('rest_framework.urls')),
    # path('api/clinics/', views.ClinicListApiView.as_view(), name='clinic_list'),
    # path('api/clinics/<int:pk>/', views.ClinicDetailApiView.as_view(), name='clinic_detail'),
    # path('api/cabinets/', views.CabinetListApiView.as_view()),
    path('api/events/', views.EventListApiView.as_view()),  # GET POST
]


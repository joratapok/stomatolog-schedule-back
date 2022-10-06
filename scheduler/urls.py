from django.urls import path, include
from . import views


urlpatterns = [
    # # Вход
    # path('/api/auth/sign_in/'),
    # # Авторизация
    # path('/api/auth/sign_up/'),
    # path('api/auth/', include('rest_framework.urls')),
    path('api/events/', views.ClinicListApiView.as_view(), name='clinic_list'),
    path('api/events/<int:pk>/', views.ClinicDetailApiView.as_view(), name='clinic_detail'),
]

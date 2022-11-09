from django.urls import path, include
from . import views

urlpatterns = [
    # # Вход
    # path('/api/auth/sign_in/', views.LoginUser.as_view(), name='login'),
    # # Авторизация
    # path('api/auth/sign_up/', views.create_employee, name='create_user'),
    path('api/events/', views.ClinicListApiView.as_view()),  # GET
    path('api/events/create/', views.EventCreateApiView.as_view()),  # POST
    path('api/profile/create/', views.ProfileCreateApiView.as_view()),  # POST

]


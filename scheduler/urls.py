from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include, re_path
from . import views


urlpatterns = [
    # # Вход пользователя
    # path('/api/auth/sign_in/', views.LoginUser.as_view(), name='login'),
    # # Регистрация нового пользователя
    # path('api/auth/sign_up/', views.create_employee, name='create_user'),

    path('api/events/', views.ClinicListApiView.as_view()),  # GET
    path('api/events/create/', views.EventCreateApiView.as_view()),  # POST

    # Регистрация нового пользователя и
    path('api/profile/create/', views.UserCreateApiView.as_view()),  # POST
    path('api/profile/<int:pk>/', views.UserRetrieveUpdateDestroyAPIView.as_view()),

    # path('api/auth/', include('djoser.urls')),
    # path('api/auth/login/', obtain_auth_token, name='token'),

    # Вход и выход по токенам
    """ Вход по 'auth/token/login' 
        Выход по 'auth/token/logout' 
    """,
    re_path(r'^auth/', include('djoser.urls.authtoken')),

]
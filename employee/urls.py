from django.urls import path, include, re_path
from employee import views

urlpatterns = [
    path('info/', views.UserRetrieveAPIView.as_view()),
    path('create/', views.UserCreateApiView.as_view()),
    path('<int:pk>/', views.UserUpdateDestroyAPIView.as_view()),

    path('login/', views.ProfileTokenCreateView.as_view()),
    path('logout/', views.ProfileTokenDestroyView.as_view()),
]

from django.urls import path
from employee import views

urlpatterns = [
    path('info/', views.ProfileRetrieveAPIView.as_view()),
    path('create/', views.ProfileCreateApiView.as_view()),
    path('<int:pk>/', views.ProfileRetrieveUpdateDestroyAPIView.as_view()),

    path('login/', views.ProfileTokenCreateView.as_view()),
    path('logout/', views.ProfileTokenDestroyView.as_view()),
]

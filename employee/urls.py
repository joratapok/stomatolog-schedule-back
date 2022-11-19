from django.urls import path, include, re_path
from employee import views

urlpatterns = [
    path('create/', views.UserCreateApiView.as_view()),
    path('<int:pk>/', views.UserRetrieveUpdateDestroyAPIView.as_view()),
    re_path(r'^auth/', include('djoser.urls.authtoken')),

]

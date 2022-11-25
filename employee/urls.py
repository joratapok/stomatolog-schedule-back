from django.urls import path, include, re_path
from employee import views

urlpatterns = [
    path('info/', views.UserRetrieveAPIView.as_view()),
    path('create/', views.UserCreateApiView.as_view()),
    path('<int:pk>/', views.UserUpdateDestroyAPIView.as_view()),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    # re_path(r'^auth/', views.ObtainExpiringAuthToken.as_view()),

]

from django.urls import path, re_path, include
from . import views


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api/events/', views.EventListApiView.as_view()),
    re_path(r'^api/events/(?P<date>\d{4}-\d{2}-\d{2})/$', views.EventListApiView.as_view(), name='event_list'),
]

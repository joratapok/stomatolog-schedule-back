from django.urls import path
from price import views

urlpatterns = [
    path('price-list/', views.PriceListCreateAPIView.as_view(), name='price-list'),
    path('price-list/<int:pk>/', views.PriceListRetrieveUpdateDestroyAPIView.as_view(), name='price-detail'),

    path('service/', views.ServiceListCreateAPIView.as_view(), name='service-list'),
    path('service/<int:pk>', views.ServiceRetrieveUpdateDestroyAPIView.as_view(), name='service-detail'),
]

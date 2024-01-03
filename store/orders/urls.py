from django.urls import path

from orders import views

app_name = 'orders'

urlpatterns = [
    path('', views.OrderListView.as_view(), name='orders_list'),
    path('order/<int:pk>/', views.OrderDetailView.as_view(), name='order'),
    path('order-create/', views.OrderCreateView.as_view(), name='order_create'),
    path('order-success/', views.SuccessTemplateView.as_view(), name='order_success'),
    path('order-canceled/', views.CanceledTemplateView.as_view(), name='order_canceled'),
]

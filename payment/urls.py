from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('create/<int:order_id>/', views.create_payment, name='create_payment'),
    path('return/<int:order_id>/', views.payment_return, name='payment_return'),
]
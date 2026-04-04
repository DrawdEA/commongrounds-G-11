from django.urls import path

from . import views

app_name = 'merchstore'

urlpatterns = [
    path('items/', views.product_list, name='product_list'),
    path('item/<int:pk>/', views.product_detail, name='product_detail'),
    path('item/add/', views.product_create, name='product_create'),
    path('item/<int:pk>/edit/', views.product_update, name='product_update'),
    path('cart/', views.cart_view, name='cart'),
    path('transactions/', views.transaction_list, name='transaction_list'),
]

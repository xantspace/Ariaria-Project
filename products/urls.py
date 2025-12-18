from django.urls import path
from . import views

app_name = 'products'  # ← THIS LINE MUST EXIST

urlpatterns = [
    path('product_list/', views.product_list, name='product_list'),
    path('<int:pk>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_view, name='cart'),
]

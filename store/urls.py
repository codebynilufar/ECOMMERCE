from django.urls import path

from .views import CategoryView, ProductView, ProductDetailView

urlpatterns = [
    path('categories/', CategoryView.as_view(), name='category'),
    path('products/', ProductView.as_view(), name='product'),
    path('products/<int:id>/', ProductDetailView.as_view(), name='detail')
]
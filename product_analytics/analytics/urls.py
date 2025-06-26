from django.urls import path
from django.views.generic import TemplateView

from .views import ProductListView

urlpatterns = [
    path('api/products/', ProductListView.as_view(), name='product-list'),
    path('', TemplateView.as_view(template_name='index.html')),
]
from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import CategoryView, GeneralView, add_to_basket

app_name = 'products'

urlpatterns = [
    path('', GeneralView.as_view(), name='main'),
    path('cat/<int:pk>/', CategoryView.as_view(), name='products'),
    path('a_t_b/', login_required(add_to_basket), name='add_to_basket'),
]

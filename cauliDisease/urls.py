from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('results/<int:pk>/', results, name='results')
]

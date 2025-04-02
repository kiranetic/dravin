from django.urls import path
from .views import QueryList

app_name = 'dialogue_engine'  # Namespace for URL reversing

urlpatterns = [
    path('queries/', QueryList.as_view(), name='query-list'),
]
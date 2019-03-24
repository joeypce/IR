from django.urls import path
from . import views

urlpatterns = [
    path('', views.searchengine_view, name='searchengine_view'),
    # path('<int:question_id>/', views.detail, name='detail'),
]
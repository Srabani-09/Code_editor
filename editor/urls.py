from django.urls import path
from .views import RunCode

urlpatterns = [
    path('run/', RunCode.as_view()),
]
from django.urls import path
from .views import LoginViews
urlpatterns = [
    path('login/',LoginViews.as_view(),name='login'),
]
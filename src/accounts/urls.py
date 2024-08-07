from django.urls import path
from .views import LoginViews
app_name = 'accounts'
urlpatterns = [
    path('login/',LoginViews.as_view(),name='login'),
]
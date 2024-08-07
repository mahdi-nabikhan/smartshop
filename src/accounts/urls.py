from django.urls import path
from .views import LoginViews,logoutview
app_name = 'accounts'
urlpatterns = [
    path('login/',LoginViews.as_view(),name='login'),
    path('logout/',logoutview,name='logout'),
]
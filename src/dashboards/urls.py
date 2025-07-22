from django.urls import path
from .views import *
app_name = 'dashboards'
urlpatterns = [
    path('admin_panel/', ManagerProfile.as_view(), name='admin_panel'),

]
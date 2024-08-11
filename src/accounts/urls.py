from django.urls import path
from .views import LoginViews,logoutview,SendVerificationCodeView,VerifyCodeView
app_name = 'accounts'
urlpatterns = [
    path('login/',LoginViews.as_view(),name='login'),
    path('logout/',logoutview,name='logout'),
    path('phone_login/',SendVerificationCodeView.as_view(),name='phone'),
    path('verify_code/<str:phone_number>/',VerifyCodeView.as_view(),name='verify_code')
]
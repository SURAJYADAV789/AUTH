from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('signup/',signup_view, name='signup'),
    path('login/',login_view, name='login'),
    path('dashboard/',dashboard_view, name='dashboard'),
    path("logout/", logout_view, name="logout"),

    # api url 

    path('api/signup/',SignupAPIView.as_view(), name="api-login"),
    path('api/login/',LoginAPIView.as_view(), name="api-signup"),
    path('api/logout/',LogoutAPIView.as_view(), name='api-logout'),
    path("api/profile/", ProfileAPIView.as_view()),

    path("api/admin/", AdminDashboardAPIView.as_view()),
    path("api/manager/", ManagerAPIView.as_view()),


]

from django.urls import path
from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('message-detection/', views.message_detection, name='message_detection'),
    path('email-detection/', views.email_detection, name='email_detection'),
]

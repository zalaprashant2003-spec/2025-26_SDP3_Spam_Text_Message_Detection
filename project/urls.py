from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    path('', views.home),
=======
    path('', views.home, name='home'),
    path('message-detection/', views.message_detection, name='message_detection'),
    path('email-detection/', views.email_detection, name='email_detection'),
>>>>>>> cfef04c (Add complete project with updated README and frontend code)
]

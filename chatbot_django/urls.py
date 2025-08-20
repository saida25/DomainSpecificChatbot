"""
URL configuration for chatbot_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
      path('', include('chatbot_app.urls')),
]

# chatbot_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_interface, name='chat_interface'),
    path('api/send_message/', views.send_message, name='send_message'),
    path('api/chat_history/<str:session_id>/', views.chat_history, name='chat_history'),
    path('api/clear_chat/<str:session_id>/', views.clear_chat, name='clear_chat'),
]
from django.urls import path
from blog import views

urlpatterns = [
    path('', views.hello_world)
]

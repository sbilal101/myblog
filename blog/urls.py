from django.urls import path
from blog import views

urlpatterns = [
    #path("", views.home, name="home"),
    path('', views.post_list, name='post_list')
]
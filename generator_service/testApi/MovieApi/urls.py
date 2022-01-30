from django.conf.urls import url
from . import views
 
urlpatterns = [
    url('movie', views.start)
]
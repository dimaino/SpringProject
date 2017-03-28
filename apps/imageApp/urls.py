from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = "index"),
    url(r'^uploadAnImage$', views.uploadImage, name = "uploadImage"),
    url(r'^showImage$', views.allImages, name = "showImage"),
]

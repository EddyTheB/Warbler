from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /webcam/
    url(r'^$', views.index, name='index'),
    # ex. /webcam/5/
    url(r'^(?P<camID>[0-9]+)/$', views.imageViewer, name='imageviewer'),
]

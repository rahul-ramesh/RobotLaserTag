from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^map/$', views.map, name='map'),
	url(r'^$', views.index, name='index'),
	url(r'^(?P<coords>[0-9]+)/add/$', views.add, name='add'),
]

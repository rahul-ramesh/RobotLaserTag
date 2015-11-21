from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^map/$', views.map, name='map'),
	url(r'^$', views.coords, name='coords'),
	url(r'^(?P<coords>[0-9]+)/(?P<name>[0-9]+)/(?P<angle>[0-9]+)/add_coords/$', views.add_coords, name='add_coords'),
	url(r'^(?P<angle>[0-9]+)/(?P<name>[0-9]+)/add_angle/$', views.add_angle, name='add_angle'),
]

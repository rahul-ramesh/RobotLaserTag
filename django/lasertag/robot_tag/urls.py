from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^map/$', views.map, name='map'),
	url(r'^$', views.index, name='index'),
	url(r'^(?P<team>[0-9])/coords/$', views.coords, name='coords'),
	url(r'^(?P<team>[0-9])/add_coords/(?P<coords>[0-9]{6})/$', views.add_coords, name='add_coords'),
	url(r'^(?P<team>[0-9])/add_angles/(?P<angle>[0-9]{3})/$', views.add_angles, name='add_angles'),
	url(r'^(?P<team>[0-9])/add_command/(?P<command>[0-9]+)/$', views.add_command, name='add_command'),
	url(r'^(?P<team>[0-9])/angles/$', views.angles, name='angles'),
	url(r'^(?P<team>[0-9])/command/$', views.command, name='command'),
	url(r'^(?P<team>[0-9])/fire/$', views.fire, name='fire'),
	url(r'^(?P<team>[0-9])/faults/$', views.faults, name='faults'),
]

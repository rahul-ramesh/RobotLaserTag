from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^map/$', views.map, name='map'),
	#url(r'^$', views.coords, name='coords'),
	url(r'^(?P<name>[0-9]+)/coords/$', views.coords, name='coords'),
	url(r'^(?P<name>[0-9]+)/(?P<coords>[0-9]+)/add_coords/$', views.add_coords, name='add_coords'),
	url(r'^(?P<name>[0-9]+)/(?P<angle>[0-9]+)/add_angles/$', views.add_angles, name='add_angles'),
	url(r'^(?P<name>[0-9]+)/angles/$', views.angles, name='angles'),
	url(r'^(?P<name>[0-9]+)/(?P<command>[0-9]+)/add_command/$', views.add_command, name='add_command'),
	url(r'^(?P<name>[0-9]+)/command/$', views.command, name='command'),
	url(r'^(?P<name>[0-9]+)/fire/$', views.fire, name='fire'),
	url(r'^(?P<name>[0-9]+)/faults/$', views.faults, name='faults'),
]

#urlpatterns = [
#	url(r'^map/$', views.map, name='map'),
#	url(r'^$', views.coords, name='coords'),
#	url(r'^(?P<coords>[0-9]+)/(?P<name>[0-9]+)/(?P<angle>[0-9]+)/add_coords/$', views.add_coords, name='add_coords'),
#	url(r'^(?P<angle>[0-9]+)/(?P<name>[0-9]+)/add_angle/$', views.add_angle, name='add_angle'),
#	url(r'^(?P<angle>[0-9]+)/(?P<name>[0-9]+)/command/$', views.add_command, name='add_command'),
#	url(r'^(?P<name>[0-9]+)/command/$', views.command, name='command'),
#]

from django.conf.urls import url

import os
from . import views

#if not(os.path.exists("db.sqlite3")):
#        os.system("sudo cp ~/class/RobotLaserTag/django/lasertag/backup.db.sqlite3 ~/class/RobotLaserTag/django/lasertag/db.sqlite3")
#        os.system("sudo python manage.py migrate")
#        os.system("sudo chmod 777 ~/class/RobotLaserTag/django/lasertag/db.sqlite3")


urlpatterns = [
	url(r'^map/$', views.map, name='map'),
	url(r'^$', views.index, name='index'),
	url(r'^(?P<team>[0-9])/coords/$', views.coords, name='coords'),
	url(r'^(?P<team>[0-9])/add_coords/(?P<coords>[0-9]{6})/$', views.add_coords, name='add_coords'),
	url(r'^(?P<team>[0-9])/add_angles/(?P<angle>[0-9]{3})/$', views.add_angles, name='add_angles'),
	url(r'^(?P<team>[0-9])/add_command/(?P<command>\w+)/$', views.add_command, name='add_command'),
	url(r'^(?P<team>[0-9])/angles/$', views.angles, name='angles'),
	url(r'^(?P<team>[0-9])/command/$', views.command, name='command'),
	url(r'^(?P<team>[0-9])/faults/$', views.faults, name='faults'),
]

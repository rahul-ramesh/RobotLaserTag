from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.core.urlresolvers import reverse
import numpy as np
import math
import random
# Create your views here.
import os

import nanotime


def map(request):
	try:
		map_list = Map.objects.order_by('-id')[0]
	except:
		map_list = "0000"
	context = {'map_list' : map_list}
	return render(request, 'map.html', context)

def coords(request, team):
	try:
		coords = Coords.objects.filter(team=team).order_by('-id')[0]
	except:
		coords = Coords(x = 0, y = 0, team = team)
		coords.save()
	context = {'coords' : str(coords)}
	return render(request, 'coords.html', context)

def add_coords(request, coords, team):
	coords = int(coords, 10)
	try:
        	latest_coords = Coords.objects.filter(team = team)[0]
	except:	
		latest_coords = Coords(team = team, x = 0, y = 0)
	latest_coords.x = coords/1000
	latest_coords.y = coords%1000
        latest_coords.save()
        return HttpResponseRedirect(reverse('index'))

def angles(request, team):
	try:
		angle = Angle.objects.filter(team=team).order_by('-id')[0]
	except:	
		angle = Angle(team = team, angle = 0)
		angle.save()
	context = {'angle' : str(angle)}
	return render(request, 'angles.html', context)

def add_angles(request, team, angle):
	try:
		latest_angle = Angle.objects.filter(team=team)[0]
		latest_angle.angle = angle
		latest_angle.save()
	except:	
		latest_angle = Angle.objects.create(team = team, angle = angle)
		#latest_angle.save()
        return HttpResponseRedirect(reverse('index'))

def command(request, team):
	try:
		command = Command.objects.filter(team = team).order_by('-id')[0]
	except:
		command = "No commands present!"
	context = {'command' : str(command)}
	return render(request, 'command.html', context)

def add_command(request, team, command):
	dist_step = 50
	angle_step = 30
	try:
		angleObj = Angle.objects.filter(team=team)[0]
	except:
		angleObj = Angle(team = team, angle = 0)

	try:
		coords = Coords.objects.filter(team = team)[0]
	except:
		coords = Coords(team = team, x = 0, y = 0)
        
	if command == "145s1s244s254s12":		#left
		angleObj.angle = (angleObj.angle + angle_step)%360

	if command == "145s254s12s1s244": 		#right
		angleObj.angle = (angleObj.angle - angle_step)%360

	if command == "145s1s244s1s244":		#front
		coords.x = coords.x + dist_step*math.sin(angleObj.angle*1.0)
		coords.y = coords.y + dist_step*math.cos(angleObj.angle*1.0)

	if command == "145s254s12s254s12":		#back
		coords.x = coords.x - dist_step*math.sin(angleObj.angle*1.0)
		coords.y = coords.y - dist_step*math.cos(angleObj.angle*1.0)

	if command == "fire":
		#fault = Fault(power = random.randrange(50,90), wheel = random.randrange(1,3), attacker = team)
		#fault = Fault(power = 50, wheel = 1, attacker = team)
		#fault.save()
		fire(int(team))
	latest_command = Command(team=team, command=command)
        latest_command.save()
        
	# log command for passive replication
	#os.system("rm log" + str(team) + ".txt && touch log" + str(team) + ".txt")
	#f = open("log" + str(team) + ".txt", 'w')
	#f.write(latest_command)
        #f.close()

	#os.system("rm backup.db.sqlite3 && cp db.sqlite3 backup.db.sqlite3")
	angleObj.save()
	coords.save()
        return HttpResponseRedirect(reverse('index'))

def faults(request, team):
	timeout = 10
	try:
		#faults = Fault.objects.filter(victim = team, when__gte=datetime.now()-timedelta(seconds=timeout)).order_by('-id')[0]
		fault = Fault.objects.filter(victim = team).order_by('-id')[0]
		#if (fault.when - nanotime.now().seconds()) > timeout:
		if (fault.when) < nanotime.now().seconds() - timeout:
			fault = "1: 3 0 0"
	except:
		fault = "" #Fault(victim = team, )
	context = {'faults' : fault}
	return render(request, 'faults.html', context)

def fire(attacker):
	victim = 1
	if attacker == 1:
		victim = 2
	epsilon = 45
	hit = 0
	coords1 = Coords.objects.filter(team = attacker).order_by('-id')[0]
	coords2 = Coords.objects.filter(team = victim).order_by('-id')[0]
	angle1 = Angle.objects.filter(team = attacker).order_by('-id')[0]
 	denominator = (coords1.x*1.0 - coords2.x*1.0)
	#os.system("echo " + str(coords1) + str(coords2) + str(angle) + " >> log.txt")
	#robots are along y axis, and attacker is pointing up
	if ((abs(denominator) < 10.0)):
		if ((abs(angle1.angle-180) < epsilon) and (coords2.y > coords1.y)):
			hit = 1
		if ((abs(angle1.angle) < epsilon) and (coords2.y < coords1.y)):
			hit = 1
	#attacker is facing along line connecting robots

	elif (angle1.angle <90):
		if (coords2.x > coords1.x and coords2.y < coords1.y):
			#if(abs(angle1.angle - math.degrees(math.atan((coords1.y*1.0 - coords2.y*1.0)/denominator))) < epsilon):
			hit = 1
		else:
			hit = 0

	elif (angle1.angle <180):
		if (coords2.x > coords1.x and coords2.y > coords1.y):
                        #if(abs(angle1.angle - math.degrees(math.atan((coords1.y*1.0 - coords2.y*1.0)/denominator)) - 90) < epsilon):
                        hit = 1

		else:
			hit = 0

	elif (angle1.angle <270):
                if (coords2.x < coords1.x and coords2.y > coords1.y):
                        #if(abs(angle1.angle - math.degrees(math.atan((coords1.y*1.0 - coords2.y*1.0)/denominator)) - 180) < epsilon):
                        hit = 1

                else:
                        hit = 0


	else:
                if (coords2.x < coords1.x and coords2.y < coords1.y):
                        #if(abs(angle1.angle - math.degrees(math.atan((coords1.y*1.0 - coords2.y*1.0)/denominator)) - 270) < epsilon):
                        hit = 1

                else:
                        hit = 0

	if (hit == 1):
		hit = 0
		#try:
                #        fault = Fault.objects.filter(victim = victim).order_by('-id')[0]
		#	fault.power = random.randrange(50,90)
		#	fault.wheel = random.randrange(1,3)
		#	fault.victim = victim
		#	fault.save()
                #except:
                fault = Fault(power = random.randrange(50,90), wheel = random.randrange(1,3), victim = victim, when = int(nanotime.now().seconds()))
                fault.save()
	return

def index(request):
	#if not(os.path.exists("db.sqlite3")):
	#	os.system("sudo cp ~/class/RobotLaserTag/django/lasertag/backup.db.sqlite3 ~/class/RobotLaserTag/django/lasertag/db.sqlite3")
	#	os.system("sudo python manage.py migrate")
	#	os.system("sudo chmod 777 ~/class/RobotLaserTag/django/lasertag/db.sqlite3")
	coords = Coords.objects.all().order_by('-id')
	angles = Angle.objects.all().order_by('-id')
	faults = Fault.objects.all().order_by('-id')
	context = {'coords' : coords, 'angles' : angles, 'faults' : faults}
	return render(request, 'index.html', context)

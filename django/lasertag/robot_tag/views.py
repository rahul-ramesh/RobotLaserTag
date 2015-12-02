from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.core.urlresolvers import reverse
import numpy as np
import math
# Create your views here.

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
		angle = Angles(team = team, angle = 0)
		angle.save()
	context = {'angle' : str(angle)}
	return render(request, 'angles.html', context)

def add_angles(request, team, angle):
	try:
		latest_angle = Angels.objects.filter(team=team)[0]
		latest_angle.angle = angle%360
	except:	
		latest_angle = Angles(team = team, angle = angle%360)
	latest_angle.save()
        return HttpResponseRedirect(reverse('index'))

def command(request, team):
	try:
		command = Command.objects.filter(team = team).order_by('-id')[0]
	except:
		command = "No commands present!"
	context = {'command' : str(command)}
	return render(request, 'command.html', context)

def add_command(request, team, command):
	#c = (''.join(command.split("s")))
	dist_step = 50
	angle_step = 30
	try:
		angle = Angle.objects.filter(team=team)[0]
	except:
		angle = Angle(team = team, angle = 0)

	try:
		coords = Coords.objects.filter(team = team)[0]
	except:
		coords = Coords(team = team, x = 0, y = 0)
        
	if command == "145s1s244s254s12":		#left
		angle = (angle + angle_step)%360
		angle.save()		
	if command == "145s254s12s1s244": 		#right
		angle = (angle - angle_step)%360
		angle.save()
	if command == "145s1s244s1s244":			#front
		coords.x = coords.x + dist_step*math.sin(angle)
		coords.y = coords.y + dist_step*math.cos(angle)

	if command == "145s254s12s254s12":		#back
		coords.x = coords.x - dist_step*math.sin(angle)
		coords.y = coords.y - dist_step*math.cos(angle)

	latest_command = Command(team=team, command=command)
        latest_command.save()
	angle.save()
	coords.save()
        return HttpResponseRedirect(reverse('index'))

def faults(request, team):i
	try:
		fault = Fault.objects.filter(attacker = team).order_by('-id')[0] #order_by('-id')[:1]
	except:
		fault = "No faults present!"
	context = {'faults' : str(fault)}
	return render(request, 'faults.html', context)

def fire(request, team):
	v = 1
	if (team == 1):
		v = 2
	
	try:
		coords1 = Coords.objects.filter(team = team).order_by('-id')[0]
		coords2 = Coords.objects.filter(team = v).order_by('-id')[0]
		angle = Angle.objects.filter(team = team).order_by('-id')[0]
	except:
		return HttpResponseRedirect(reverse('index'))

	slope = 0
	if (coords2.x - coords1.x != 0):
		slope = (coords2.y - coords1.y)*1.0/(coords2.x - coords1.x)

	if (math.tan(angle.angle*1.0) == slope):
		#target hit
		fault = Fault(fault_type=team, attacker=team)
		fault.save()
        return HttpResponseRedirect(reverse('index'))

def index(request):
	coords = Coords.objects.all().order_by('-id')
	angles = Angle.objects.all().order_by('-id')
	context = {'coords' : coords, 'angles' : angles}
	return render(request, 'index.html', context)

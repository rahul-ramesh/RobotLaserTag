from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.core.urlresolvers import reverse
import numpy as np
import math
# Create your views here.

def map(request):
	map_list = Map.objects.order_by('-id')[0]
	context = {'map_list' : map_list}
	return render(request, 'map.html', context)

def coords(request, team):
	coords = Coords.objects.filter(team=team).order_by('-id')[0]
	context = {'coords' : str(coords)}
	return render(request, 'coords.html', context)

def add_coords(request, coords, team):
	coords = int(coords, 10)
        latest_coords = Coords.objects.filter(team = team)
	print latest_coords
	try:
		latest_coords = latest_coords[0]
	except:	
		latest_coords = Coords.objects.create(team = team, x = 0, y = 0)
	latest_coords.x = coords/1000
	latest_coords.y = coords%1000
        latest_coords.save()
        return HttpResponseRedirect(reverse('index'))

def angles(request, team):
	angle = Angle.objects.filter(team=team).order_by('-id')[0]
	context = {'angle' : str(angle)}
	return render(request, 'angles.html', context)

def add_angles(request, team, angle):
	latest_angle = Angle.objects.filter(team = team)
	try:
		latest_angles = latest_coords[0]
	except:	
		latest_angles = Angle.objects.create(team = team, angle=0)
        latest_angles.angle = angle
	latest_angles.save()
        return HttpResponseRedirect(reverse('index'))

def command(request, team):
	command = Command.objects.filter(team = team).order_by('-id')[0]
	context = {'command' : str(command)}
	return render(request, 'command.html', context)

def add_command(request, team, command):
	#c = (''.join(command.split("s")))
	dist_step = 50
	angle_step = 30
        if command == "145s1s244s254s12":		#left
		angle = Angle.objects.filter(team=team)[0]
		angle = (angle + angle_step)%360
		angle.save()		
	if command == "145s254s12s1s244": 		#right
		angle = Angle.objects.filter(team = team)[0]
		angle = (angle - angle_step)%360
		angle.save()
	if command == "145s1s244s1s244":			#front
		coords = Coords.objects.filter(team = team)[0]
		coords.x = coords.x + dist_step*math.sin(angle)
		coords.y = coords.y + dist_step*math.cos(angle)

	if command == "145s254s12s254s12":		#back
		coords = Coords.objects.filter(team = team)[0]
		coords.x = coords.x - dist_step*math.sin(angle)
		coords.y = coords.y - dist_step*math.cos(angle)

	latest_command = Command(team=team, command=command)
        latest_command.save()
        return HttpResponseRedirect(reverse('index'))

def faults(request, team):
	fault = Fault.objects.filter(attacker = team).order_by('-id')[0] #order_by('-id')[:1]
	context = {'faults' : str(fault)}
	return render(request, 'faults.html', context)

def fire(request, team):
	v = 1
	if (team == 1):
		v = 2
	coords1 = Coords.objects.filter(team = team).order_by('-id')[0] #order_by('-id')[:1]
	coords2 = Coords.objects.filter(team = v).order_by('-id')[0] #order_by('-id')[:1]
	angle = Angle.objects.filter(team = team).order_by('-id')[0] #order_by('-id')[:1]

	slope = 0
	#coeff = np.polyfit([coords1.x coords1.y], [coords2.x coords2.y], 1)
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

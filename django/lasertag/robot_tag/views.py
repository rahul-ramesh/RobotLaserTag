from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.core.urlresolvers import reverse
import numpy as np
# Create your views here.

def map(request):
	map_list = Map.objects.order_by('-id')[:1]
	context = {'map_list' : map_list}
	return render(request, 'map.html', context)

def coords(request, name):
	coords = Coords.objects.filter(name = name).order_by('-id')[:1] #order_by('-id')[:1]
	context = {'coords' : str(coords)}
	return render(request, 'coords.html', context)

def add_coords(request, coords, name):
	coords = int(coords, 10)
        latest_coords = Coords(name, coords/1000, coords%1000)
        latest_coords.save()
        return HttpResponseRedirect(reverse('coords'))

def angles(request, name):
	angle = Angle.objects.filter(name = name).order_by('-id')[:1] #order_by('-id')[:1]
	context = {'angle' : str(angle)}
	return render(request, 'angles.html', context)

def add_angles(request, name, angle):
        latest_angles = Angle(name, angle)
        latest_angles.save()
        return HttpResponseRedirect(reverse('angle'))

def command(request, name):
	command = Command.objects.filter(name = name).order_by('-id')[:1] #order_by('-id')[:1]
	context = {'command' : str(command)}
	return render(request, 'command.html', context)

def add_command(request, name, command):
        latest_command = Command(name, command)
        latest_command.save()
        return HttpResponseRedirect(reverse('command'))

def faults(request, name):
	fault = fault.objects.filter(name = name).order_by('-id')[:1] #order_by('-id')[:1]
	context = {'faults' : str(fault)}
	return render(request, 'faults.html', context)

def fire(request, name):
	coords1 = Coords.objects.filter(name = 1).order_by('-id')[:1] #order_by('-id')[:1]
	coords2 = Coords.objects.filter(name = 2).order_by('-id')[:1] #order_by('-id')[:1]
	angle = Angle.objects.filter(name = n).order_by('-id')[:1] #order_by('-id')[:1]

	#coeff = np.polyfit([coords1.x coords1.y], [coords2.x coords2.y], 1)
	slope = (coords2.y - coords1.y)*1.0/(coords2.x - coords1.x)
	if (math.tan(angle) == 	slope):
		#target hit
		fault = Fault(1, n)
		fault.save()
        return HttpResponseRedirect(reverse('faults'))

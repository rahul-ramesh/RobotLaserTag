from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.core.urlresolvers import reverse

# Create your views here.

def coords(request):
	coords1 = Coords.objects.filter(team = 1).order_by('-id')[:1] #order_by('-id')[:1]
	coords2 = Coords.objects.filter(team = 2).order_by('-id')[:1]
	angle1 = Angle.objects.filter(team = 1).order_by('-id')[:1] #order_by('-id')[:1]
	angle2 = Angle.objects.filter(team = 2).order_by('-id')[:1]
	context = {'coords1' : str(coords1), 'coords2' : str(coords2), 'angle1' : str(angle1), 'angle2' : str(angle2)}
	return render(request, 'coords.html', context)

def map(request):
	map_list = Map.objects.order_by('-id')[:1]
	context = {'map_list' : map_list}
	return render(request, 'map.html', context)

def add_coords(request, coords, name):
	coords = int(coords, 10)
        latest_coords = Coords(name, coords/1000, coords%1000)
        latest_coords.save()
        return HttpResponseRedirect(reverse('coords'))

def add_angle(request, angle, name):
        latest_angles = Angle(name, angle)
        latest_angles.save()
        return HttpResponseRedirect(reverse('coords'))


from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.core.urlresolvers import reverse

# Create your views here.

def index(request):
	coords = Coords.objects.order_by('-id')[:1]
	context = {'coords' : coords}
	print coords
	return render(request, 'coords.html', context)

def map(request):
	map_list = Map.objects.order_by('-id')[:1]
	context = {'map_list' : map_list}
	return render(request, 'map.html', context)

def add(request,coords):
	coords = int(coords, 10)
        latest_coords = Coords(name="robot_name", x=coords/1000, y=coords%1000)
        latest_coords.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('index'))

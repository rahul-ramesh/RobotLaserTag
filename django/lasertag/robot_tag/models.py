from django.db import models
# Create your models here.

class Map(models.Model):
	map = models.CharField(max_length=10000)
	x = models.IntegerField(default = 100)
	y = models.IntegerField(default = 100)
	def __str__(self):
		return self.map

	def getMap(self, xpos, ypos):
		return self.map(xpos*x + ypos)

class Coords(models.Model):
	team = models.IntegerField(default = 1)
	x = models.IntegerField(default = 0)
	y = models.IntegerField(default = 0)

	def __str__(self):
		return str(self.team) + ': ' + str(self.x) + ' ' + str(self.y) + ' ' 
	
class Angle(models.Model):
	team = models.IntegerField(default = 1)
	angle = models.IntegerField(default = 0)

	def __str__(self):
		return str(self.team) + ': ' + str(self.angle) + ' '

class Command(models.Model):
	command = models.CharField(max_length = 20, default = "fire")
	team = models.IntegerField(default = 1)

	def __str__(self):
		return str(self.team) + ': ' + str(self.command) + ' ' + str(self.id) + ' '
	
class Fault(models.Model):
	power = models.IntegerField(default = 1)
	wheel = models.IntegerField(default = 1)
	victim = models.IntegerField(default=1)
	#when = models.DateTimeField(auto_now = True)
	when = models.IntegerField(default = 1)
	def __str__(self):
		return str(self.victim) + ': ' + str(self.wheel) + ' ' + str(self.power)+ ' ' + str(self.id) + ' '
	

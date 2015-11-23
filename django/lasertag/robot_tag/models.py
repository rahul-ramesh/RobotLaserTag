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
	team = models.CharField(max_length = 20, default = 1)
	command = models.IntegerField(default = 0)

	def __str__(self):
		return str(self.team) + ': ' + str(self.command) + ' ' + str(self.id) + ' '
	
class Fault(models.Model):
	fault_type = models.IntegerField(default = 1)
	attacker = models.IntegerField(default=1)

	def __str__(self):
		return str(self.attacker) + ': ' + str(self.fault_type) + ' ' + str(self.id) + ' '
	

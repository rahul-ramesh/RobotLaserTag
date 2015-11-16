from django.db import models

# Create your models here.

class Map(models.Model):
	map = models.CharField(max_length=100)

	def __str__(self):
		return self.map


class Coords(models.Model):
	name = models.CharField(max_length = 10)
	team = models.IntegerField(default = 1)
	x = models.IntegerField(default = 0)
	y = models.IntegerField(default = 0)

	def __str__(self):
		return '' + str(self.x) + ' ' + str(self.y)  + ' ' + self.name

class Fault(models.Model):
	fault_type = models.IntegerField(default = 1)
	victim = models.IntegerField(default=1)
	attacker = models.IntegerField(default=1)

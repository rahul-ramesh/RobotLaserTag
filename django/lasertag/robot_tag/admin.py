from django.contrib import admin

# Register your models here.


from .models import Fault
from .models import Map
from .models import Coords

admin.site.register(Fault)
admin.site.register(Map)
admin.site.register(Coords)

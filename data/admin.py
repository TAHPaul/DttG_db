from django.contrib import admin
from .models import (
	Colour, 
	City, 
	Museum, 
	Artist, 
	Artwork, 
	Data
	)

# Register your models here.
admin.site.register(Colour)
admin.site.register(City)
admin.site.register(Museum)
admin.site.register(Artist)
admin.site.register(Artwork)
admin.site.register(Data)
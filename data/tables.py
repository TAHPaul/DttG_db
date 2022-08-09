import django_tables2 as tables
from .models import (
    Colour, 
    City, 
    Museum, 
    Artist, 
    Artwork, 
    Data
    )

class ArtistTable(tables.Table):
    class Meta:
        model = Artist
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", "full_name", "place_of_birth", "place_of_death", "year_of_birth", "year_of_death", "rkd_link", "image", )
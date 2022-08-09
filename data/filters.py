import django_filters
from django_filters import NumberFilter

from .models import *

class ArtworkFilter(django_filters.FilterSet):
	start_date = NumberFilter(field_name="date1", lookup_expr='gte') #OR date2 gte to start_date
	end_date = NumberFilter(field_name="date1", lookup_expr='lte') #OR date2 lte to start_date

	class Meta:
		model = Artwork 
		fields = ["artist1", "artist2", "place_of_execution", "data__layer1_colour", "data__layer2_colour", "data__layer3_colour", "data__toplayer_colour"]
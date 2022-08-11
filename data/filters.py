import django_filters
from django_filters import NumberFilter, CharFilter, ChoiceFilter

from .models import *

COLOUR_GROUPS = (
		('Yellow', 'Yellow'),
		('White', 'White'),
		('Red', 'Red'),
		('Pink', 'Pink'),
		('Orange', 'Orange'),
		('Grey', 'Grey'),
		('Black', 'Black'),
		('Brown', 'Brown'),
	)

class ArtworkFilter(django_filters.FilterSet):
	artist = CharFilter(
		field_name="artist1__full_name", 
		#field_name="artist2", 
		lookup_expr='icontains',
		label="Artist")

	start_date = NumberFilter(
		field_name="date1", 
		lookup_expr='gte', 
		label="Created after"
		) #OR date2 gte to start_date
	
	end_date = NumberFilter(
		field_name="date1", 
		lookup_expr='lte', 
		label="Made before"
		) #OR date2 lte to start_date
	
	place_of_execution = CharFilter(
		field_name="place_of_execution__city",
		lookup_expr='icontains',
		label="City of Execution")

	toplayer_colour = ChoiceFilter(
		choices= COLOUR_GROUPS,
		field_name="data__toplayer_colour__group",
		lookup_expr='exact',
		label="Colour of uppermost ground",
		)

	lowestlayer_colour = ChoiceFilter(
		choices= COLOUR_GROUPS,
		field_name="data__layer1_colour__group",
		lookup_expr='exact',
		label="Colour of lowest ground",
		)

	class Meta:
		model = Artwork 
		fields = ["data__layer1_colour", "data__layer2_colour", "data__layer3_colour", "data__toplayer_colour"]
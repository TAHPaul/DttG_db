from django import forms
from .models import *

import django_filters

# Uses the django_filters python plug-in to create a slightly more sophisticated search function
# that allows for picking multiple options (e.g. artists, cities of execution) - so that complex
# queries can be initiated.

class AdvancedSearch(django_filters.FilterSet):
    artist = django_filters.ModelMultipleChoiceFilter(
        queryset=Artist.objects.all().order_by('full_name'),
        field_name='artist1__id',
        to_field_name='id', 
        label='Artist(s)'
    )

    city = django_filters.ModelMultipleChoiceFilter(
        queryset=City.objects.exclude(execution_city=None).order_by('city'),
        field_name='place_of_execution__city',
        to_field_name='city', 
        label='City of Execution'
    )

# For now the date range filter only applies to date 1, as the django_filters plug-in does not yet
# support an OR statement (e.g. date1 < x OR date2 < x)
    date1 = django_filters.RangeFilter(
        field_name='date1',
        label='Date range')

    GROUND_NO = (
        ('1', 'One'),
        ('2', 'Two'),
        ('3', 'Three'),
        ('4', 'Four'),
        ('5', 'Five'),
        ('6', 'Six'),
        ('7', 'Seven'),
        ('8', 'Eight'),
        ('9', 'Nine'),
        ('10', 'Ten'),
        ('>10', 'More than ten')
    )

    no_of_grounds = django_filters.MultipleChoiceFilter(
    	field_name='data__no_of_grounds',
        choices=GROUND_NO,
    	label="# of Grounds")

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

    bottomlayer = django_filters.MultipleChoiceFilter(
    	field_name='data__layer1_colour__group',
    	choices=COLOUR_GROUPS,
    	label='Colour of bottom ground layer'
    	) 

    toplayer = django_filters.MultipleChoiceFilter(
    	field_name='data__toplayer_colour__group',
    	choices=COLOUR_GROUPS,
    	label='Colour of topmost ground layer'
    	)

    reliability = django_filters.NumberFilter(
    	field_name='data__reliability',
    	lookup_expr='lte',
    	label='Min. Reliability'
    	)

    support = django_filters.AllValuesMultipleFilter(
    	field_name='support',
    	label='Support'
    	)

    medium = django_filters.AllValuesMultipleFilter(
        field_name='medium',
        label='Medium'
        )

# Here we give options for the analysis part of the painting. this is not 
# yet filled in for most data entries so might be redundant at this point?

    sampled = django_filters.AllValuesMultipleFilter(
    	field_name='data__sample',
    	label='Sampled?'
    	)

    microscopy = django_filters.AllValuesMultipleFilter(
    	field_name='data__microscopy',
    	label='Microscopy?'
    	)

    elem_analysis = django_filters.AllValuesMultipleFilter(
    	field_name='data__elem_analysis',
    	label='Elemental Analysis?')

# The ordering options, more can be added by simply adding the relevant field as a tuple to the list.
    o = django_filters.OrderingFilter(
    	fields=(
    		('artist1', 'artist'),
    		('city', 'city'),
    		('date1', 'date'),
    		('data__no_of_grounds', '# ground layers'),
    		('data__layer1_colour__group', 'bottom ground layer colour'),
    		('data__toplayer_colour__group', 'top ground layer colour'),
   		),
   		label='Order by:'
    )   

    class Meta:
        model = Artwork
        fields = [
        	'artist', 
        	'city',
        	'date1',
        	'no_of_grounds', 
        	'bottomlayer', 
        	'toplayer', 
        	'reliability',
        	'medium',
        	'support', 
        	'sampled', 
        	'microscopy', 
        	'elem_analysis'
        ]










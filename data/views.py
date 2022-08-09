from django.shortcuts import render
from .models import (
    Colour, 
    City, 
    Museum, 
    Artist, 
    Artwork, 
    Data
    )
from django.views.generic import(
    ListView,
    DetailView
    )
import folium

from .tables import ArtistTable

from django_tables2 import SingleTableView

from .filters import ArtworkFilter

###OTHER###...................................###OTHER###

def enter(request):
	return render(request, 'data/entry-page.html')

def home(request):
	return render(request, 'data/dttg-home.html')

def about(request):
	return render(request, 'data/dttg-about.html')

def team(request):
	return render(request, 'data/dttg-team.html')

def colours(request):
    context = {
        'colours': Colour.objects.all().order_by('group'),
        'title': 'Colours',
        'black': Colour.objects.get(colour_name='Black'),
        'white': Colour.objects.get(colour_name='White'),
    }
    return render(request, 'data/colours.html', context)


def reliability(request):
    return render(request, 'data/reliability.html')

###ARTISTS###...............................###ARTISTS###

class ArtistListView(ListView):
    model = Artist
    context_object_name = 'artists'
    ordering = ['id']
    paginate_by = 9
    artists = Artist.objects.all()

    global no_of_artists 
    no_of_artists = len(artists)

    def get_context_data(self, **kwargs):
        context = super(ArtistListView, self).get_context_data(**kwargs)
        context['no_of_artists'] = no_of_artists
        return context

class ArtistDetailView(DetailView):
    model = Artist
    #how to give title of page?

###MUSEUMS###...............................###MUSEUMS###

class MuseumListView(ListView):
    #global m
    #m = folium.Map(width=800, height=500)

    #for museum in Museum.objects.all():
       #if museum.city.latitude: 
            #folium.Marker([museum.city.latitude, museum.city.longitude]).add_to(m)

    #folium.Marker([43.2,-121.4]).add_to(m)

    #m = m._repr_html_()

    model = Museum
    context_object_name = 'museums'
    ordering = ['id']
    paginate_by = 15
    museums = Museum.objects.all()

    global no_of_museums
    no_of_museums = len(museums)

    def get_context_data(self, **kwargs):
        context = super(MuseumListView, self).get_context_data(**kwargs)
        context['no_of_museums'] = no_of_museums
        return context

    #def get_context_data(self, **kwargs):
        #context = super(MuseumListView, self).get_context_data(**kwargs)
        #context['map'] = m
        #return context

class MuseumDetailView(DetailView):
    model = Museum

###DATA###.....................................###DATA###
class DataListView(ListView):
    model = Data
    context_object_name = 'data'
    ordering = ['m_number']
    paginate_by = 12

    entries = Data.objects.all()

    global no_of_entries
    no_of_entries = len(entries)

    def get_context_data(self, **kwargs):
        context = super(DataListView, self).get_context_data(**kwargs)
        context['no_of_entries'] = no_of_entries
        return context

class DataDetailView(DetailView):
    model = Data

def data_table(request):
    artworks = Artwork.objects.all()

    myFilter = ArtworkFilter(request.GET, queryset=artworks)
    artworks = myFilter.qs

    results = len(artworks)

    context = {
        'artworks': artworks,
        #'artwork1': Artwork.objects.first(),
        'tablenames': Artwork._meta.get_fields(),
        'myFilter': myFilter,
        'results': results, 
        }      

    return render(request, 'data/table.html', context)

###CITIES###.................................###CITIES###

def city_of_execution_overview(request):
    context = {
        'cities': City.objects.all(),
    }    

    return render(request, 'data/city-of-execution-overview.html', context)

class city_of_execution_detail(DetailView):
	model = City
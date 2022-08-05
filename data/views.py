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
        'colours': Colour.objects.all(),
        'title': 'Colours',
    }
    return render(request, 'data/colours.html', context)


def reliability(request):
    return render(request, 'data/reliability.html')

###ARTISTS###...............................###ARTISTS###

class ArtistListView(ListView):
    model = Artist
    context_object_name = 'artists'
    ordering = ['id']
    paginate_by = 20
    #'o': Artist.objects.get(id=115).artist.count()

    #how to give title of page?

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
    paginate_by = 20

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
    paginate_by = 20

class DataDetailView(DetailView):
    model = Data

def data_table(request):
	return render(request, 'data/data-table.html')

###CITIES###.................................###CITIES###

def city_of_execution_overview(request):
    context = {
        'cities': City.objects.all(),
    }    

    return render(request, 'data/city-of-execution-overview.html', context)

class city_of_execution_detail(DetailView):
	model = City
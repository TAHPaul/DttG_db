from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse
from statistics import mean
import csv

# import all models from the models.py file
from .models import (
    Colour, 
    City, 
    Museum, 
    Artist, 
    Artwork, 
    Data
    )

# import generated views native to Django
from django.views.generic import(
    ListView,
    DetailView
    )

# imports the advancedsearch form for the table querying, from forms.py
from .forms import AdvancedSearch


#  OTHER...................................OTHER

def home(request):
	return render(request, 'data/dttg-home.html')

def about(request):
	return render(request, 'data/dttg-about.html')

def db_info(request):
    context = {
        'colours': Colour.objects.all().order_by('group'),
        'title': 'Colours',
        'black': Colour.objects.get(colour_name='Black'),
        'white': Colour.objects.get(colour_name='White'),
    }
    return render(request, 'data/db-info.html', context)

#  ARTISTS...............................ARTISTS

class ArtistListView(ListView):
    model = Artist
    context_object_name = 'artists'
    ordering = ['id']
    paginate_by = 9
    artists = Artist.objects.all().order_by('full_name')

    global no_of_artists 
    no_of_artists = len(artists)

    def get_context_data(self, **kwargs):
        context = super(ArtistListView, self).get_context_data(**kwargs)
        context['no_of_artists'] = no_of_artists
        return context

class ArtistDetailView(DetailView):
    model = Artist

#  MUSEUMS...............................MUSEUMS

class MuseumListView(ListView):
    model = Museum
    context_object_name = 'museums'
    ordering = ['id']
    paginate_by = 15
    museums = Museum.objects.all().order_by('museum_name')

    global no_of_museums
    no_of_museums = len(museums)

    def get_context_data(self, **kwargs):
        context = super(MuseumListView, self).get_context_data(**kwargs)
        context['no_of_museums'] = no_of_museums
        return context

class MuseumDetailView(DetailView):
    model = Museum

#  DATA.....................................DATA
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

def data_table_simple(request):
    artworks = Artwork.objects.all()

    if 'artist' in request.GET:
        artist = request.GET['artist']
        artworks = Artwork.objects.filter(Q(artist1__full_name__icontains=artist) | Q(artist2__full_name__icontains=artist))
    else:
        artworks = artworks

    if 'date1' in request.GET:
        date1 = request.GET['date1']
        if date1:
            artworks = artworks.filter(Q(date1__gte=date1) | Q(date2__gte=date1))
        else:
            artworks = artworks

    if 'date2' in request.GET:
        date2 = request.GET['date2']
        if date2:
            artworks = artworks.filter(Q(date1__lte=date2) | Q(date2__lte=date2))
        else:
            artworks = artworks

    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            artworks = artworks.filter(place_of_execution__city__icontains=city)
        else:
            artworks = artworks

    if 'no_of_grounds' in request.GET:
        no_of_grounds = request.GET['no_of_grounds']
        if no_of_grounds:
            artworks = artworks.filter(data__no_of_grounds__iexact=no_of_grounds)
        else:
            artworks = artworks

    if 'support' in request.GET:
        support = request.GET['support']
        if support:
            if support =='any':
                artworks = artworks
            if support == 'canvas':
                artworks = artworks.filter(support__icontains='canvas')
            if support == 'panel':
                artworks = artworks.filter(support__icontains='panel')
            if support == 'other':
                artworks = artworks.filter(~Q(support__icontains='canvas') & ~Q(support__icontains='panel'))
            if support == 'unknown':
                artworks = artworks.filter(support__iexact='')
        else:
            artworks = artworks


    if 'sortby' in request.GET:
        sortby = request.GET['sortby']
        if sortby == 'ID':
            artworks = artworks.order_by('id')
        elif sortby == 'Title':
            artworks = artworks.order_by('title')
        elif sortby == 'Artist':
            artworks = artworks.order_by('artist1', 'date1')
        elif sortby == 'Date':
            artworks = artworks.order_by('date1', 'date2')
        elif sortby == 'Place of execution':
            artworks = artworks.order_by('place_of_execution', 'date1')
        elif sortby == '# grounds':
            artworks = artworks.order_by('data__no_of_grounds')
        elif sortby == 'Lowest ground':
            artworks = artworks.order_by('data__layer1_colour__group', 'data__layer1_colour__id')
        elif sortby == 'Uppermost ground':
            artworks = artworks.order_by('data__toplayer_colour__group', 'data__toplayer_colour__id')

    artworks = artworks.distinct()
    results=len(artworks)

    context={
        'artworks': artworks,
        'tablenames': Artwork._meta.get_fields(),
        'results': results,
    }
    
    return render(request, 'data/table_simple_query.html', context)

def csv_export_simple(request):
    artworks = Artwork.objects.all()
    
    if 'artist' in request.GET:
        artist = request.GET['artist']
        artworks = Artwork.objects.filter(Q(artist1__full_name__icontains=artist) | Q(artist2__full_name__icontains=artist))
    else:
        artworks = artworks

    if 'date1' in request.GET:
        date1 = request.GET['date1']
        if date1:
            artworks = artworks.filter(Q(date1__gte=date1) | Q(date2__gte=date1))
        else:
            artworks = artworks

    if 'date2' in request.GET:
        date2 = request.GET['date2']
        if date2:
            artworks = artworks.filter(Q(date1__lte=date2) | Q(date2__lte=date2))
        else:
            artworks = artworks

    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            artworks = artworks.filter(place_of_execution__city__icontains=city)
        else:
            artworks = artworks

    if 'no_of_grounds' in request.GET:
        no_of_grounds = request.GET['no_of_grounds']
        if no_of_grounds:
            artworks = artworks.filter(data__no_of_grounds__iexact=no_of_grounds)
        else:
            artworks = artworks

    if 'sortby' in request.GET:
        sortby = request.GET['sortby']
        if sortby == 'ID':
            artworks = artworks.order_by('id')
        elif sortby == 'Title':
            artworks = artworks.order_by('title')
        elif sortby == 'Artist':
            artworks = artworks.order_by('artist1')
        elif sortby == 'Date':
            artworks = artworks.order_by('date1')
        elif sortby == 'Place of execution':
            artworks = artworks.order_by('place_of_execution')
        elif sortby == '# grounds':
            artworks = artworks.order_by('data__no_of_grounds')
        elif sortby == 'Lowest ground':
            artworks = artworks.order_by('data__layer1_colour__group')
        elif sortby == 'Uppermost ground':
            artworks = artworks.order_by('data__toplayer_colour__group')

    artworks = artworks.distinct()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=DttG_simple_query.csv'

    writer = csv.writer(response)

    writer.writerow([
        'ID', 
        'Title', 
        'Artist validity', 
        'Artist', 
        'Secondary artist', 
        'Place of execution', 
        'Date validity', 
        'Date 1', 
        'Date 2',
        'Date bin (5 years)',
        'Date bin (10 years)',
        'Number of grounds',
        'Description',
        'Toplayer Colour',
        'Layer 1 colour',
        'Layer 1 composition',
        'Layer 2 colour',
        'Layer 2 composition',
        'Layer 3 colour',
        'Layer 3 composition',
        'Reliability',
        'Researchers',
        'Source'
    ])

    for entry in artworks:
        if entry.artist2:
            artist2 = entry.artist2.full_name
        else:
            artist2 = ''

        if entry.data.layer1_colour:
            layer1 = entry.data.layer1_colour.colour_name
        else:
            layer1 = ''

        if entry.data.layer2_colour:
            layer2 = entry.data.layer2_colour.colour_name
        else:
            layer2 = ''

        if entry.data.layer3_colour:
            layer3 = entry.data.layer3_colour.colour_name
        else:
            layer3 = ''

        if entry.date2:
            date_list = [entry.date2, entry.date1]
            date_av = mean(date_list)
            date_bin5 = int((date_av // 5) * 5)
            date_bin10 = int((date_av // 10) * 10)
        else: 
            date_av = entry.date1
            date_bin5 = int((date_av //5) * 5)
            date_bin10 = int((date_av // 10) * 10)

        writer.writerow([
            entry.id, 
            entry.title, 
            entry.artist_validity, 
            entry.artist1.full_name,
            artist2,
            entry.place_of_execution,
            entry.date_validity,
            entry.date1,
            entry.date2,
            date_bin5,
            date_bin10,
            entry.data.no_of_grounds,
            entry.data.description,
            entry.data.toplayer_colour,
            layer1,
            entry.data.layer1_composition,
            layer2,
            entry.data.layer2_composition,
            layer3,
            entry.data.layer3_composition,
            entry.data.reliability,
            entry.data.researchers,
            entry.data.source
            ])

    return response

def data_table_advanced(request):
    advancedsearch = AdvancedSearch(request.GET, queryset=Artwork.objects.all())

    context={
        'advancedsearch': advancedsearch,
        'results': len(advancedsearch.qs),
    }
    
    return render(request, 'data/table_advanced_query.html', context)

def csv_export_adv(request):
    entries = Artwork.objects.all()

    qs = AdvancedSearch(request.GET, queryset=entries).qs

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=DttG_adv_query.csv'

    #create a csv writer
    writer = csv.writer(response)
    
    # Add column headings to csv file
    writer.writerow([
        'ID', 
        'Title', 
        'Artist validity', 
        'Artist', 
        'Secondary artist', 
        'Place of execution', 
        'Date validity', 
        'Date 1', 
        'Date 2',
        'Date bin (5 years)',
        'Date bin (10 years)', 
        'Number of grounds',
        'Description',
        'Toplayer Colour',
        'Layer 1 colour',
        'Layer 1 composition',
        'Layer 2 colour',
        'Layer 2 composition',
        'Layer 3 colour',
        'Layer 3 composition',
        'Reliability',
        'Researchers',
        'Source'
    ])

    for entry in qs:
        if entry.artist2:
            artist2 = entry.artist2.full_name
        else:
            artist2 = ''

        if entry.data.layer1_colour:
            layer1 = entry.data.layer1_colour.colour_name
        else:
            layer1 = ''

        if entry.data.layer2_colour:
            layer2 = entry.data.layer2_colour.colour_name
        else:
            layer2 = ''

        if entry.data.layer3_colour:
            layer3 = entry.data.layer3_colour.colour_name
        else:
            layer3 = ''

        if entry.date2:
            date_list = [entry.date2, entry.date1]
            date_av = mean(date_list)
            date_bin5 = int((date_av // 5) * 5)
            date_bin10 = int((date_av // 10) * 10)
        else: 
            date_av = entry.date1
            date_bin5 = int((date_av //5) * 5)
            date_bin10 = int((date_av // 10) * 10)

        writer.writerow([
            entry.id, 
            entry.title, 
            entry.artist_validity, 
            entry.artist1.full_name,
            artist2,
            entry.place_of_execution,
            entry.date_validity,
            entry.date1,
            entry.date2,
            date_bin5,
            date_bin10,
            entry.data.no_of_grounds,
            entry.data.description,
            entry.data.toplayer_colour,
            layer1,
            entry.data.layer1_composition,
            layer2,
            entry.data.layer2_composition,
            layer3,
            entry.data.layer3_composition,
            entry.data.reliability,
            entry.data.researchers,
            entry.data.source
            ])

    return response

#  CITIES.................................CITIES

def city_of_execution_overview(request):
    context = {
        'cities': City.objects.all().order_by('country', 'city')
    }    

    return render(request, 'data/city-of-execution-overview.html', context)

class city_of_execution_detail(DetailView):
	model = City
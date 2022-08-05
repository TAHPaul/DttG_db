from django.urls import path
from . import views
from .views import (
	ArtistListView,
	ArtistDetailView,
	MuseumListView,
	MuseumDetailView,
	) # FOR THE LISTVIEW

urlpatterns = [
	path('', views.enter, name='entry_page'),
	path('home/', views.home, name='dttg-home'),
	path('about/', views.about, name='dttg-about'),
	path('team/', views.team, name='dttg-team'),
	path('artists/', ArtistListView.as_view(), name='artists-overview'), #NEW LIST VIEW
	path('artists/<int:pk>/', views.ArtistDetailView.as_view(), name='artists-detail'),
	path('entries/', views.DataListView.as_view(), name='data-overview'),
	path('entries/<str:pk>/', views.DataDetailView.as_view(), name='data-detail'),
	path('entries-table/', views.data_table, name='data-table'),
	path('museums/', views.MuseumListView.as_view(), name='museums-overview'),
	path('museums/<int:pk>/', views.MuseumDetailView.as_view(), name='museums-detail'),
	path('colours/', views.colours, name='colours'),
	path('city-of-execution/', views.city_of_execution_overview, name='city-of-execution-overview'),
	path('city-of-execution/<str:pk>/', views.city_of_execution_detail.as_view(), name='city-of-execution-detail'),
	path('reliability/', views.reliability, name='reliability')
]

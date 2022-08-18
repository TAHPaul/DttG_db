from django.urls import path
from . import views
from .views import (
	ArtistListView,
	ArtistDetailView,
	MuseumListView,
	MuseumDetailView,
	) # FOR THE LISTVIEW

urlpatterns = [
	path('', views.home, name='dttg-home'),
	path('about/', views.about, name='dttg-about'),
	path('artists/', ArtistListView.as_view(), name='artists-overview'), #NEW LIST VIEW
	path('artists/<int:pk>/', views.ArtistDetailView.as_view(), name='artists-detail'),
	path('entries/', views.DataListView.as_view(), name='data-overview'),
	path('entries/<str:pk>/', views.DataDetailView.as_view(), name='data-detail'),
	path('entries-table-adv/', views.data_table_advanced, name='data-table-adv'),
	path('entries-table-adv/export_csv', views.csv_export_adv, name='csv-export-adv'),
	path('entries-table-simple/', views.data_table_simple, name='data-table-simple'),
	path('entries-table-simple/export-csv', views.csv_export_simple, name='csv-export-simple'),
	path('museums/', views.MuseumListView.as_view(), name='museums-overview'),
	path('museums/<int:pk>/', views.MuseumDetailView.as_view(), name='museums-detail'),
	path('db_info/', views.db_info, name='database-info'),
	path('city-of-execution/', views.city_of_execution_overview, name='city-of-execution-overview'),
	path('city-of-execution/<str:pk>/', views.city_of_execution_detail.as_view(), name='city-of-execution-detail'),
]

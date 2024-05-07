from data.models import Artist, City, Museum, Artwork, Colour, Data
from pathlib import Path
import csv

def run():
	with open('data/csv/artists.csv') as file:
		reader = csv.reader(file)
		next(reader) #to advance past the headers

		for row in reader:
			print("Data entry:", row)

			try:
				yob = int(row[5])
			except ValueError:
				yob = None #ensures that if no year_of_birth is given, a valid empty cell is created.

			try:
				yod = int(row[6])
			except ValueError:
				yod = None #ensures that if no year_of_death is given, a valid empty cell is created.

			qs = Artist.objects.filter(id=row[0])

			if qs: #checks if the entry exists
				print("Artist:", str(row[1]), "already exists in database. Will check and update values.\n")
				artist = Artist.objects.get(id=row[0])
				artist.full_name=row[1]
				artist.other_names=row[2]
				artist.place_of_birth=City.objects.get(city=row[3])
				artist.place_of_death=City. objects.get(city=row[4])
				artist.year_of_birth=yob 
				artist.year_of_death=yod 
				artist.centres_of_activity=row[7]
				artist.rkd_link=row[8]
				artist.save()
				print("Artist:", str(row[1]), "updated.\n")		
			else: #if it doesn't exist, a new entry is made.
				artist = Artist(id=row[0],
								full_name=row[1],
								other_names=row[2],
								place_of_birth=City.objects.get(city=row[3]),
								place_of_death=City.objects.get(city=row[4]),
								year_of_birth=yob,
								year_of_death=yod,
								centres_of_activity=row[7],
								rkd_link=row[8]
								)
				artist.save()
				print("Artist:", str(row[1]), "added to database\n")

			

			
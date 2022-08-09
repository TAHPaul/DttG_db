from data.models import Artist, City, Museum, Artwork, Colour, Data
import csv

def run():
	with open('data/csv/artists.csv') as file:
		reader = csv.reader(file)
		next(reader) #to advance past the headers

		for row in reader:
			print(row)

			try:
				yob = int(row[5])
			except ValueError:
				yob = None #ensures that if no year_of_birth is given, a valid empty cell is created.

			try:
				yod = int(row[6])
			except ValueError:
				yod = None #ensures that if no year_of_death is given, a valid empty cell is created.

			qs = Artist.objects.filter(id=row[0])

			if qs:
				print("Artist", str(row[1]), "already exists in database\n")
				#checks if the entry doesn't already exist.
			else:
				artist = Artist(id=row[0],
								full_name=row[1],
								other_names=row[2],
								place_of_birth=City.objects.get(city=row[3]),
								place_of_death=City.objects.get(city=row[4]),
								year_of_birth=yob,
								year_of_death=yod,
								centres_of_activity=row[7],
								rkd_link=row[8])

				artist.save()
				print("artist", str(row[1]), "added to database\n")
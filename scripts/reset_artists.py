from data.models import Artist, City, Museum, Artwork, Colour, Data
from pathlib import Path
import csv

def run():
	with open('data/csv/artists.csv') as file:
		reader = csv.reader(file)
		next(reader) #to advance past the headers

		check = 'a'
		while check == 'a':
			check = input("Are you sure you want to delete all your artist entries? This will delete related artist images. This is non-reversible. [y/n] : ")

			if check.lower().startswith("y"):
				print("Continuing.")
				continue
			elif check.lower().startswith("n"):
				print("Okay, good we checked... Closing the script.")
				exit()
			else:
				check = 'a'
				continue

		Artist.objects.all().delete()
		print("All artists deleted.\n Adding new entries...\n")

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

			

			
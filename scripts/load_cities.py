from data.models import Artist, City, Museum, Artwork, Colour, Data
import csv

def run():
	with open('data/csv/cities.csv') as file:
		reader = csv.reader(file)
		next(reader) #to advance past the headers

		for row in reader:
			print("Data entry:", row)
			qs = City.objects.filter(city=row[0])

			try:
				lat = float(row[3])
			except ValueError:
				lat = None #ensures that if no year_of_birth is given, a valid empty cell is created.

			try:
				lon = float(row[4])
			except ValueError:
				lon = None #ensures that if no year_of_birth is given, a valid empty cell is created.

			if qs:
				print("City:", str(row[0]), "already exists in database. Will update values.")
				city = City.objects.get(city=row[0])
				city.country=row[1]
				city.continent=row[2]
				city.latitude=lat
				city.longitude=lon
				city.save()
				print("City:", str(row[0]), "updated.\n")
			else:
				city = City(city=row[0],
							country=row[1],
							continent=row[2],
							latitude=lat,
							longitude=lon) 
				city.save()
				print("City:", str(row[0]), "added to database\n")
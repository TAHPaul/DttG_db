from data.models import Artist, City, Museum, Artwork, Colour, Data
import csv

def run():
	with open('data/csv/museums.csv') as file:
		reader = csv.reader(file)
		next(reader) #to advance past the headers

		for row in reader:
			print(row)
			
		
			qs = Museum.objects.filter(id=row[0])

			if qs:
				print("Museum", str(row[1]), "already exists in database\n")
				#checks if the artwork does not already exist in the database
			else:
				museum = Museum(id=row[0],
								museum_name=row[1],
								website=row[2],
								city=City.objects.get(id=row[3])

				museum.save()
				print("Museum", str(row[1]), "added to database\n")
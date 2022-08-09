from data.models import Artist, City, Museum, Artwork, Colour, Data
import csv

def run():
	with open('data/csv/cities.csv') as file:
		reader = csv.reader(file)
		next(reader) #to advance past the headers

		for row in reader:
			print(row)
						
			qs = City.objects.filter(id=row[0])

			if qs:
				print("City", str(row[1]), "already exists in database\n")
				#checks if the artwork does not already exist in the database
			else:
				city = City(city=row[0],
							country=row[1],
							continent=row[2],
							latitude=row[3],
							longitude=row[4]) 

				city.save()
				print("City", str(row[1]), "added to database\n")
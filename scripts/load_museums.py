from data.models import Artist, City, Museum, Artwork, Colour, Data
import csv

# function that reads the csv, scrolls through the rows and inserts the data-entries
def run():
	with open('data/csv/museums.csv') as file:
		reader = csv.reader(file)
		next(reader) #to advance past the headers

		for row in reader:
			print("Data entry:", row)
			qs = Museum.objects.filter(id=row[0])

			if row[2]:
				city = City.objects.get(city=row[2])
			else:
				city = None
			#checks if the artwork does not already exist in the database
			if qs:
				print("Museum:", str(row[1]), "already exists in database. Will update values.")
				museum = Museum.objects.get(id=row[0])
				museum.museum_name=row[1]
				museum.city=city
				museum.website=row[3]
				museum.save()
				print("Museum:", str(row[1]), "updated.\n")
			# if the entry doesn't exist yet - a new one is created	
			else:
				museum = Museum(id=row[0],
								museum_name=row[1],
								city=city,
								website=row[3])

				museum.save()
				print("Museum:", str(row[1]), "added to database\n")
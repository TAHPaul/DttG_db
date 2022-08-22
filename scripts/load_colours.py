from data.models import Artist, City, Museum, Artwork, Colour, Data
import csv

def run():
	with open('data/csv/colours.csv') as file:
		reader = csv.reader(file)
		next(reader) #to advance past the headers

		for row in reader:
			print(row)
			
			qs = Colour.objects.filter(id=row[0])

			if qs:
				print("Colour", str(row[1]), "already exists in database\n")
				#checks if the artwork does not already exist in the database
			else:
				colour = Colour(id=row[0],
								colour_name=row[1],
								hex_code=row[2],
								group=row[3])

			colour.save()
			print("Colour", str(row[1]), "added to database\n")
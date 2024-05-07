from data.models import Artist, City, Museum, Artwork, Colour, Data
import csv

def run():
	with open('data/csv/cities.csv') as file:
		reader = csv.reader(file)
		next(reader) #to advance past the headers

		check = 'a'
		while check == 'a':
			check = input("Are you sure you want to reset all your city entries? This is non-reversible. [y/n] : ")

			if check.lower().startswith("y"):
				print("Continuing.")
				continue
			elif check.lower().startswith("n"):
				print("Okay, good we checked... Closing the script.")
				exit()
			else:
				check = 'a'
				continue

		City.objects.all().delete()
		print("All cities deleted.\n Adding new entries...\n")

		for row in reader:
			print("Data entry:", row)

			try:
				lat = float(row[3])
			except ValueError:
				lat = None #ensures that if no latitude is given, a valid empty cell is created.

			try:
				lon = float(row[4])
			except ValueError:
				lon = None #ensures that if no longitude is given, a valid empty cell is created.

			city = City(city=row[0],
						country=row[1],
						continent=row[2],
						latitude=lat,
						longitude=lon) 
			city.save()
			print("City:", str(row[0]), "added to database\n")
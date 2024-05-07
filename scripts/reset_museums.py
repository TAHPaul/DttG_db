from data.models import Artist, City, Museum, Artwork, Colour, Data
import csv

# function that reads the csv, scrolls through the rows and inserts the data-entries
def run():
	with open('data/csv/museums.csv') as file:
		reader = csv.reader(file)
		next(reader) #to advance past the headers

		check = 'a'
		while check == 'a':
			check = input("Are you sure you want to delete all your museum entries? This is non-reversible. [y/n] : ")

			if check.lower().startswith("y"):
				print("Continuing.")
				continue
			elif check.lower().startswith("n"):
				print("Okay, good we checked... Closing the script.")
				exit()
			else:
				check = 'a'
				continue

		Museum.objects.all().delete()
		print("All museums deleted.\n Adding new entries...\n")

		for row in reader:
			print("Data entry:", row)

			if row[2]:
				city = City.objects.get(city=row[2])
			else:
				city = None

			museum = Museum(id=row[0],
							museum_name=row[1],
							city=city,
							website=row[3])
			museum.save()
			print("Museum:", str(row[1]), "added to database\n")
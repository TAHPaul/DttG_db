from data.models import Artist, City, Museum, Artwork, Colour, Data
import csv

def run():
	with open('data/csv/colours.csv') as file:
		reader = csv.reader(file)
		next(reader) #to advance past the headers

		check = 'a'
		while check == 'a':
			check = input("Are you sure you want to reset all your colour entries? This is non-reversible. [y/n] : ")

			if check.lower().startswith("y"):
				print("Continuing.")
				continue
			elif check.lower().startswith("n"):
				print("Okay, good we checked... Closing the script.")
				exit()
			else:
				check = 'a'
				continue

		Colour.objects.all().delete()
		print("All colours deleted.\n Adding new entries...\n")

		for row in reader:
			print("Data entry:", row)
			
			colour = Colour(id=row[0],
							colour_name=row[1],
							hex_code=row[2],
							group=row[3])
			colour.save()
			print("Colour:", str(row[1]), "added to database\n")
			
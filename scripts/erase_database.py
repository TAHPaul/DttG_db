from data.models import Artist, City, Museum, Artwork, Colour, Data

def run():
	print("This script will delete all data from the database. This is a non-reversible action.\n")

	check = 'a'
	while check == 'a':
		check = input("Are you sure you want to proceed? This is the only check [y/n] : ")

		if check.lower().startswith("y"):
			print("Continuing.")
			continue
		elif check.lower().startswith("n"):
			print("Okay, good we checked... Closing the script.")
			exit()
		else:
			check = 'a'
			continue

	Data.objects.all().delete()
	print("All data entries deleted.")
	Artwork.objects.all().delete()
	print("All data artwork deleted.")
	Artist.objects.all().delete()
	print("All data artist deleted.")
	Museum.objects.all().delete()
	print("All data museum deleted.")
	City.objects.all().delete()
	print("All data city deleted.")
	Colour.objects.all().delete()
	print("All data colour deleted.\n")
	print("Database empty.")


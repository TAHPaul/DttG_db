from data.models import Artist, City, Museum, Artwork, Colour, Data
import csv

def run():
	with open('data/csv/artworks.csv') as file:
		reader = csv.reader(file)
		next(reader) #to advance past the headers

		for row in reader:
			print("Data entry:", row)
			
			#These try functions ensure valid empty cells get added if certain fields are missing
			try: #artist2
				a2 = Artist.objects.get(id=row[4])
			except ValueError:
				a2 = None

			try: #date1
				d1 = int(row[7])
			except ValueError:
				d1 = None

			try: #date2
				d2 = int(row[8])
			except ValueError:
				d2 = None

			try: #height
				h = float(row[14])
			except ValueError:
				h = None

			try: #width
				w = float(row[15])
			except ValueError:
				w = None

			if row[17] == '': #if no museum is entered, it gets museum entry 49 which is 'unknown'
				m = Museum.objects.get(id=49)
			else:
				m = Museum.objects.get(id=row[17])
			
			qs = Artwork.objects.filter(id=row[0])

			if qs:
				print("Artwork:", str(row[1]), "already exists in database. Will check and update values.\n")
				artwork = Artwork.objects.get(id=row[0])
				artwork.title=row[1]
				artwork.artist_validity=row[2]
				artwork.artist1=Artist.objects.get(id=row[3])
				artwork.artist2=a2
				artwork.place_of_execution=City.objects.get(city=row[5])
				artwork.date_validity=row[6]
				artwork.date1=d1
				artwork.date2=d2
				artwork.signature=row[11]
				artwork.support=row[12]
				artwork.medium=row[13]
				artwork.height=h
				artwork.width=w
				artwork.accession_number=row[16]
				artwork.museum=m
				artwork.museum_link=row[18]
				artwork.rkd_link=row[19]
				artwork.save()
				print("Artwork:", str(row[1]), "updated.\n")
				#checks if the artwork does not already exist in the database
			else:
				artwork = Artwork(id=row[0],
								title=row[1],
								artist_validity=row[2],
								artist1=Artist.objects.get(id=row[3]),
								artist2=a2,
								place_of_execution=City.objects.get(city=row[5]),
								date_validity=row[6],
								date1=d1,
								date2=d2,
								signature=row[11],
								support=row[12],
								medium=row[13], 
								height=h, 
								width=w, 
								accession_number=row[16], 
								museum=m, 
								museum_link=row[18], 
								rkd_link=row[19]) 
				artwork.save()
				print("Artwork:", str(row[1]), "added to database\n")
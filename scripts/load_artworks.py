from data.models import Artist, City, Museum, Artwork, Colour, Data
import csv

def run():
	with open('data/csv/artworks.csv') as file:
		reader = csv.reader(file)
		next(reader) #to advance past the headers

		for row in reader:
			print(row)
			
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
				h = float(row[12])
			except ValueError:
				h = None

			try: #width
				w = float(row[13])
			except ValueError:
				w = None

			if row[15] == '': #if no museum is entered, it gets museum entry 49 which is 'unknown'
				m = Museum.objects.get(id=49)
			else:
				m = Museum.objects.get(id=row[15])
			
			qs = Artwork.objects.filter(id=row[0])

			if qs:
				print("Artwork", str(row[1]), "already exists in database\n")
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
								signature=row[9],
								support=row[10],
								medium=row[11], 
								height=h, 
								width=w, 
								accession_number=row[14], 
								museum=m, 
								museum_link=row[16], 
								rkd_link=row[17]) 

			artwork.save()
			print("Artwork", str(row[1]), "added to database\n")
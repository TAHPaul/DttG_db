from data.models import Artist, City, Museum, Artwork, Data, Colour
import csv

def run():
	with open('data/csv/data.csv', encoding="utf8") as file:
		reader = csv.reader(file)
		next(reader) #to advance past the headers

		for row in reader:
			print(row)

			
			#if functions to ensure proper formatting of empty cells.
			if row[4] == '':
				c1 = None
			else:
				c1 = Colour.objects.get(id=row[4])

			if row[6] == '':
				c2 = None
			else:
				c2 = Colour.objects.get(id=row[6])

			if row[8] == '':
				c3 = None
			else:
				c3 = Colour.objects.get(id=row[8])

			if row[10] == '':
				tc = None
			else:
				tc = Colour.objects.get(id=row[10])
			
			#queryset to check if the data entry already exists in the database
			qs = Data.objects.filter(m_number=row[0])

			if qs:
				print("Data entry", str(row[0]), "already exists in database\n")
			else:
				data = Data(m_number=Artwork.objects.get(id=row[0]),
								no_of_grounds = row[1],
								description = row[2],
								colour_code = row[3],
								layer1_colour = c1,
								layer1_composition = row[5],
								layer2_colour = c2,
								layer2_composition = row[7],
								layer3_colour = c3,
								layer3_composition = row[9],
								toplayer_colour = tc,
								reliability = row[11],
								sample = row[12],
								microscopy = row[13],
								elem_analysis = row[14],
								sample_location = row[15],
								sample_name_1 = row[16],
								sample_link_1 = row[17],
								sample_name_2 = row[18],
								sample_link_2 = row[19],
								researchers = row[20],
								source = row[21],
								dttg_new_research = row[22],
								notes = row[23])

				data.save()
				print("Data entry", str(row[0]), "added to database\n")
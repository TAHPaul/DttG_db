from data.models import Artist, City, Museum, Artwork, Colour, Data
import csv

# function that reads the csv, scrolls through the rows and inserts the data-entries
def run():
	with open('data/csv/data.csv', encoding="utf8") as file:
		reader = csv.reader(file)
		next(reader) #to advance past the headers

		for row in reader:
			print("Data entry:", row)			
			#if functions to ensure proper formatting of empty cells.
			if row[7] == '':
				c1 = None
			else:
				c1 = Colour.objects.get(id=row[7])

			if row[9] == '':
				c2 = None
			else:
				c2 = Colour.objects.get(id=row[9])

			if row[11] == '':
				c3 = None
			else:
				c3 = Colour.objects.get(id=row[11])

			if row[13] == '':
				tc = None
			else:
				tc = Colour.objects.get(id=row[13])
			
			qs = Data.objects.filter(m_number=row[0])
			#checks if the artwork does not already exist in the database
			if qs:
				print("Data entry:", str(row[0]), "already exists in database. Will check and update values.\n")
				data = Data.objects.get(m_number=row[0])
				data.no_of_grounds = row[1]
				data.description = row[2]
				data.colour_code = row[3]
				data.layer1_colour = c1
				data.layer1_composition = row[8]
				data.layer2_colour = c2
				data.layer2_composition = row[10]
				data.layer3_colour = c3
				data.layer3_composition = row[12]
				data.toplayer_colour = tc
				data.reliability = row[14]
				data.sample = row[15]
				data.microscopy = row[16]
				data.elem_analysis = row[17]
				data.sample_location = row[18]
				data.sample_name_1 = row[19]
				data.sample_link_1 = row[20]
				data.sample_name_2 = row[21]
				data.sample_link_2 = row[22]
				data.researchers = row[23]
				data.source = row[24]
				data.dttg_new_research = row[25]
				data.notes = row[26]
				data.save()
				print("Data entry:", str(row[1]), "updated.\n")
			# if the entry doesn't exist yet - a new one is created	
			else:
				data = Data(m_number=Artwork.objects.get(id=row[0]),
								no_of_grounds = row[1],
								description = row[2],
								colour_code = row[3],
								layer1_colour = c1,
								layer1_composition = row[8],
								layer2_colour = c2,
								layer2_composition = row[10],
								layer3_colour = c3,
								layer3_composition = row[12],
								toplayer_colour = tc,
								reliability = row[14],
								sample = row[15],
								microscopy = row[16],
								elem_analysis = row[17],
								sample_location = row[18],
								sample_name_1 = row[19],
								sample_link_1 = row[20],
								sample_name_2 = row[21],
								sample_link_2 = row[22],
								researchers = row[23],
								source = row[24],
								dttg_new_research = row[25],
								notes = row[26])
				data.save()
				print("Data entry:", str(row[0]), "added to database\n")
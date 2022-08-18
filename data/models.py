from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
import os
from PIL import Image

# Create your models here.
class Colour(models.Model):
	COLOUR_IDS = (
        ('LW', 'LW'),
        ('W', 'W'),
        ('DW', 'DW'),
        ('LBl', 'LBl'),
        ('Bl', 'Bl'),
        ('DBl', 'DBl'),
        ('LR', 'LR'),
        ('R', 'R'),
        ('DR', 'DR'),
        ('LY', 'LY'),
        ('Y', 'Y'),
        ('DY', 'DY'),
        ('LBr', 'LBr'),
        ('Br', 'Br'),
        ('DBr', 'DBr'),
        ('LP', 'LP'),
        ('P', 'P'),
        ('DP', 'DP'),
        ('LO', 'LO'),
        ('O', 'O'),
        ('DO', 'DO'),
        ('LG', 'LG'),
        ('G', 'G'),
        ('DG', 'DG'),
    )

	COLOUR_GROUPS = (
		('Yellow', 'Yellow'),
		('White', 'White'),
		('Red', 'Red'),
		('Pink', 'Pink'),
		('Orange', 'Orange'),
		('Grey', 'Grey'),
		('Black', 'Black'),
		('Brown', 'Brown'),
	)
	id = models.CharField(max_length=3, choices=COLOUR_IDS, primary_key=True)
	colour_name = models.CharField(max_length=20)
	hex_code = models.CharField(max_length=7)
	group = models.CharField(max_length=10, choices=COLOUR_GROUPS)

	def __str__(self):
		return self.colour_name

class City(models.Model):
	city = models.CharField(max_length=40, primary_key=True)
	country = models.CharField(max_length=40, blank=True)
	continent = models.CharField(max_length=40, blank=True)
	latitude = models.DecimalField(decimal_places=7, max_digits=9, blank=True, null=True)
	longitude = models.DecimalField(decimal_places=7, max_digits=9, blank=True, null=True)

	class Meta:
		verbose_name_plural = 'Cities'

	def __str__(self):
		return self.city

class Museum(models.Model):
	id = models.PositiveSmallIntegerField(primary_key=True) 
	museum_name = models.CharField(max_length=50, unique=True)
	website = models.URLField(blank=True)
	city = models.ForeignKey(City, on_delete=models.SET('city was deleted'), blank=True, null=True)

	def __str__(self):
		return '%s. %s' % (self.id, self.museum_name)

def artist_file_name(self, filename):
	ext = filename.split('.')[-1]
	filename = "%s.%s" % (self.id, ext)

	return os.path.join('artist_images', filename)

class Artist(models.Model):
	id = models.PositiveSmallIntegerField(primary_key=True) 
	full_name = models.CharField(max_length=50, unique=True, help_text="Please format: LASTNAME, firstname")
	other_names = models.TextField(blank=True, help_text="Please format: LASTNAME, firstname | LASTNAME, firstname | etc.")
	place_of_birth = models.ForeignKey(City, on_delete=models.SET('city was deleted'), related_name='birth_place', blank = True) 
	place_of_death = models.ForeignKey(City, on_delete=models.SET('city was deleted'), related_name='death_place', blank = True) 
	year_of_birth = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(2022)], blank = True, null = True, default=None)
	year_of_death = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(2022)], blank = True, null = True, default=None)
	centres_of_activity = models.TextField(blank=True, help_text="Please format: City1 | City2 | City3 | etc. ")
	rkd_link = models.URLField(blank=True)
	image = models.ImageField(default='artist_images/default_artist.jpg', upload_to=artist_file_name)

	def __str__(self):
		return '%s' % (self.full_name)

	def save(self):
		super().save()

		img = Image.open(self.image.path)
		
		if img.height >300 or img.width >300:
			output_size = (300,300)
			img.thumbnail(output_size)
			img.save(self.image.path)

def artwork_file_name(self, filename):
	ext = filename.split('.')[-1]
	filename = "%s.%s" % (self.id, ext)

	return os.path.join('artwork_images', filename)

class Artwork(models.Model):
	ARTIST_VALIDITY = (
        ('copy after', 'Copy after'),
        ('in the style of', 'In the style of'),
        ('uncertain', 'Uncertain'),
        ('attributed to', 'Attributed to'),
        ('NULL', 'NULL'),
        ('Workshop of', 'Workshop of')
    )

	DATE_VALIDITY = (
		('c.', 'Circa'),
        ('decade', 'Decade'),
        ('in or shortly after', 'In or shortly after'),
        ('after', 'After'),
        ('before', 'Before'),
	)

	OPTIONS = (
		('yes', 'YES'),
    	('no', 'NO'),
    	('unclear', 'UNCLEAR'),
    )

	SUPPORTS = (
		('canvas', 'Canvas'),
    	('panel', 'Panel'),
    	('panel transferred to canvas', 'Panel transferred to canvas'),
    	('copper', 'Copper'),
    	('canvas on panel', 'Canvas on panel'),
    )

	id = models.CharField(primary_key=True, max_length=6, help_text="Please use the following formatting: M###")
	title = models.CharField(max_length=200)
	artist_validity = models.CharField(max_length=30, choices=ARTIST_VALIDITY, blank=True)
	artist1 = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='artist')
	artist2 = models.ForeignKey(Artist, on_delete=models.CASCADE, blank=True, null=True, related_name='secondary_artist')
	place_of_execution = models.ForeignKey(City, on_delete=models.SET('city was deleted'), related_name='execution_city')
	date_validity = models.CharField(max_length=30, choices=DATE_VALIDITY, blank=True)
	date1 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(2022)])
	date2 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(2022)], blank=True, null=True)
	signature = models.CharField(max_length=10, choices=OPTIONS, blank=True)
	support = models.CharField(max_length=40, choices=SUPPORTS, blank=True)
	medium = models.CharField(max_length=50, blank=True)
	height = models.DecimalField(decimal_places=2, max_digits=6, blank=True, null=True)
	width = models.DecimalField(decimal_places=2, max_digits=6, blank=True, null=True)
	accession_number = models.CharField(max_length=40, blank=True)
	museum = models.ForeignKey(Museum, models.SET('museum was deleted'), related_name='artwork_museum')
	museum_link = models.URLField(blank=True)
	rkd_link = models.URLField(blank=True)
	image = models.ImageField(default='artwork_images/default_artwork.jpg', upload_to=artwork_file_name)

	def __str__(self):
		return '%s, %s, %s' % (self.id, self.artist1, self.title)

	def save(self):
		super().save()

		img = Image.open(self.image.path)
		
		if img.height >600 or img.width >600:
			output_size = (600,600)
			img.thumbnail(output_size)
			img.save(self.image.path)

def sample1df_name(self, filename):
	ext = filename.split('.')[-1]
	filename = "%s_1_DF.%s" % (self.m_number.id, ext)

	return os.path.join('sample_images', str(self.m_number.id), filename)

def sample1bf_name(self, filename):
	ext = filename.split('.')[-1]
	filename = "%s_1_BF.%s" % (self.m_number.id, ext)

	return os.path.join('sample_images', str(self.m_number.id), filename)

def sample1uv_name(self, filename):
	ext = filename.split('.')[-1]
	filename = "%s_1_UV.%s" % (self.m_number.id, ext)

	return os.path.join('sample_images', str(self.m_number.id), filename)

def sample2df_name(self, filename):
	ext = filename.split('.')[-1]
	filename = "%s_2_DF.%s" % (self.m_number.id, ext)

	return os.path.join('sample_images', str(self.m_number.id), filename)

def sample2bf_name(self, filename):
	ext = filename.split('.')[-1]
	filename = "%s_2_BF.%s" % (self.m_number.id, ext)

	return os.path.join('sample_images', str(self.m_number.id), filename)

def sample2uv_name(self, filename):
	ext = filename.split('.')[-1]
	filename = "%s_2_UV.%s" % (self.m_number.id, ext)

	return os.path.join('sample_images', str(self.m_number.id), filename)

class Data(models.Model):
	GROUND_NO = (
		('1', 'One'),
		('2', 'Two'),
		('3', 'Three'),
	)

	OPTIONS = (
    	('yes', 'YES'),
    	('no', 'NO'),
    	('unclear', 'UNCLEAR'),
    )

	m_number = models.OneToOneField(Artwork, on_delete=models.CASCADE, primary_key=True)
	no_of_grounds = models.CharField(choices=GROUND_NO, max_length=1, blank=True)
	description = models.TextField(blank=True)
	colour_code = models.CharField(max_length=10, blank=True)
	layer1_colour = models.ForeignKey(Colour, on_delete=models.PROTECT, related_name='colour_1', null=True, blank=True)
	layer1_composition = models.TextField(blank=True)
	layer2_colour = models.ForeignKey(Colour, on_delete=models.PROTECT, related_name='colour_2', null=True, blank=True)
	layer2_composition = models.TextField(blank=True)
	layer3_colour = models.ForeignKey(Colour, on_delete=models.PROTECT, related_name='colour_3', null=True, blank=True)
	layer3_composition = models.TextField(blank=True)
	toplayer_colour = models.ForeignKey(Colour, on_delete=models.PROTECT, related_name='colour_toplayer', null=True, blank=True)
	reliability = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], blank=True, null=True)
	sample = models.CharField(max_length=10, choices=OPTIONS, blank=True)
	microscopy = models.CharField(max_length=10, choices=OPTIONS, blank=True)
	elem_analysis = models.CharField(max_length=10, choices=OPTIONS, blank=True)
	sample_location = models.TextField(blank=True)
	sample_name_1 = models.CharField(max_length=50, blank=True)
	sample_link_1 = models.URLField(blank=True)
	sample_name_2 = models.CharField(max_length=50, blank=True)
	sample_link_2 = models.URLField(blank=True)
	researchers = models.TextField(blank=True)
	source = models.TextField(blank=True)
	dttg_new_research = models.CharField(max_length=10, choices=OPTIONS, blank=True)
	notes = models.TextField(blank=True)
	sample1df = models.ImageField(default='', upload_to=sample1df_name, blank=True)
	sample1bf = models.ImageField(default='', upload_to=sample1bf_name, blank=True)
	sample1uv = models.ImageField(default='', upload_to=sample1uv_name, blank=True)
	sample2df = models.ImageField(default='', upload_to=sample2df_name, blank=True)
	sample2bf = models.ImageField(default='', upload_to=sample2bf_name, blank=True)
	sample2uv = models.ImageField(default='', upload_to=sample2uv_name, blank=True)
	embargo = models.BooleanField(default=False)

	class Meta:
		verbose_name_plural = 'Data'

	def __str__(self):
		return '%s %s' % (self.m_number.id, self.m_number.title)

	def save(self):
		super().save()
		if self.sample1df:
			img1 = Image.open(self.sample1df.path)
			
			if img1.height >700 or img1.width >700:
				output_size = (700,700)
				img1.thumbnail(output_size)
				img1.save(self.sample1df.path)

		if self.sample1bf:
			img2 = Image.open(self.sample1bf.path)
			
			if img2.height >700 or img2.width >700:
				output_size = (700,700)
				img2.thumbnail(output_size)
				img2.save(self.sample1bf.path)

		if self.sample1uv:
			img3 = Image.open(self.sample1uv.path)
			
			if img3.height >700 or img3.width >700:
				output_size = (700,700)
				img3.thumbnail(output_size)
				img3.save(self.sample1uv.path)

		if self.sample2df:
			img4 = Image.open(self.sample2df.path)
			
			if img4.height >700 or img4.width >700:
				output_size = (700,700)
				img4.thumbnail(output_size)
				img4.save(self.sample2df.path)

		if self.sample2bf:
			img5 = Image.open(self.sample2bf.path)
			
			if img5.height >700 or img5.width >700:
				output_size = (700,700)
				img5.thumbnail(output_size)
				img5.save(self.sample2bf.path)

		if self.sample2uv:
			img6 = Image.open(self.sample2uv.path)
			
			if img6.height >700 or img6.width >700:
				output_size = (700,700)
				img6.thumbnail(output_size)
				img6.save(self.sample2uv.path)
import os

def artist_file_name(self, filename):
	ext = filename.split('.')[-1]
	filename = "%s.%s" % (self.id, ext)

	return os.path.join('artist_images', filename)

def artwork_file_name(self, filename):
	ext = filename.split('.')[-1]
	filename = "%s.%s" % (self.id, ext)

	return os.path.join('artwork_images', filename)

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
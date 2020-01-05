import os

class BaseFolder:
	def __init__(self,directory,extension):
		self.directory = directory
		self.extension = extension
		self.list_of_files = os.listdir(directory)

	def __nonzero__(self):
		return bool(self.list_of_files)

	def __iter__(self):
		return self.list_of_files.__iter__()

	def __repr__(self):
		return f"directory: {self.directory}\nnummber of files: {len(self.list_of_files)}\nextensions: .{self.extension}"




class FolderTxt(BaseFolder):

	def search_for_matches(self,user_bag_of_words):
		approptiate_file_names = []
		for txt_f in self.list_of_files: # grabbing all txt files in the directory
		    f = open(self.directory+txt_f,"r")
		    text = set(f.read().split()) # getting a bag of words from the txt files
		    if user_bag_of_words.issubset(text): # check if the user input is a subset of the bag of words
		    	approptiate_file_names.append(txt_f)
		    	f.close()
		return approptiate_file_names


class FolderImg(BaseFolder):

	def img_name(self,file_name):
		'''Returns the string that represents the relative path for an image'''

		full_file_name = file_name+"."+self.extension
		if full_file_name in self.list_of_files:
			return self.directory+full_file_name

		raise KeyError("There is no file like that")
		


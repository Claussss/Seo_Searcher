import os

class BaseFolder:
	def __init__(self,directory,extension):
		self.directory = directory
		self.extension = extension
		self.list_of_files = os.listdir(directory)


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

	def open_img(self,file_name):

		full_file_name = file_name+"."+self.extension
		if full_file_name in self.list_of_files:
			return open(self.directory+full_file_name,'rb')

		raise KeyError("There is no file like that")
		
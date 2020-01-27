import os
from collections import Counter

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

	
	def __init__(self,*args):
		super().__init__(*args)

		self.content_of_txt_files = {}

		self.list_of_all_words = []

		for file_name in self.list_of_files: # grabbing all txt files in the directory
		    with open(self.directory+file_name,"r") as f:
		    	file_content = f.read()
		    	self.content_of_txt_files[file_name] = set(file_content.split()) # bag_of_words_of_txt_file
		    	self.list_of_all_words+=file_content.split()

		counter_of_all_words = sorted(Counter(self.list_of_all_words))
		for i in counter_of_all_words: # STopped here
			print(i)

		    	 


	def search_for_matches(self,user_bag_of_words):
		approptiate_file_names = [file_name for file_name in self.content_of_txt_files if self.content_of_txt_files[file_name].issuperset(user_bag_of_words)]
		return approptiate_file_names


class FolderImg(BaseFolder):

	def path_to_img(self,file_name):
		'''Returns the string that represents the relative path for an image'''

		full_file_name = file_name+"."+self.extension
		if full_file_name in self.list_of_files:
			return self.directory+full_file_name

		raise KeyError("There is no file like that")
		

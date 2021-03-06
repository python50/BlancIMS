
"""
	BlancIMS - Open Source Inventory Management
	http://github.com/python50/BlancIMS
	
	The goal of BlancIMS is to create a readily available, easy to use 
	solution for small inventory management task. In specific it was created
	for use by Jason White during the Gannon Programming Contest to keep
	track of his rather large collection electronic components he has
	amassed for his hobbies of electronics and robotics.
	
	BlancIMS Copyright (C) 2013 Jason White
	This project is licensed under GPLv2.
"""

import cPickle
import string
import pprint
import csv

""" item():
	The humble item, A data storage class
	
	Also used as a the category container class 
"""
class item():	
	def __init__(self, parent, model="", contents=None, manufacturer="", description="", quantity=0, cost=0, location=""):
		self.parent=parent
		
		#if possible add itself to its parent
		#if it is not already in its parents list
		
		if self.parent!=self and self.parent!=None:
			if self.parent.contents:
				found=0
				for i in self.parent.contents:
					if i==self:
						found=1
				if found==0:
					self.parent.contents.append(self)
			else:
				self.parent.contents=[self]
			
		
		#if a list of the category contents is provided the item is treated as a category)
		#if None is provided then the item is  is treated as a generic item
		self.contents=contents
		
		#The name of the category or model number of the item
		self.model=str(model)
		
		#who made it
		self.manufacturer=str(manufacturer)
		
		#The decription of the item
		self.description=str(description)
		
		#The quanity of the item
		self.quantity=int(quantity)
		
		self.cost=float(cost)
		
		self.location=str(location)
		
		
	def is_category(self):
		if self.contents==None:
			return False
		return True
		
	#returns the string NAME of the category
	def get_category(self):
		if self.parent!=None:
			return self.parent.model
		
	def to_csv_exclusive(self):
		text=""
		for i in self.contents:
			text=text+i.model+","+i.description+","+i.quantity+"\n"
			
		return text
		
		
""" BlancDB_Manager():
	Provides an interface for:
		adding
		removing

		loading
		saving
		
		TBA importing to csv
		TBA exporting to csv
	items from the item list
"""	
class BlancDB_Manager():
	def __init__(self):
		self.db=BlancDB_Writer()
		self.root=item(parent=None, model="Root", contents=[])
		self.root.parent=self.root
		
	def report(self, text):
		#
		print "BlancDB_Manager(): "+str(text)
		
	def clear(self):
		self.root.contents=[]
		
		
	#Dump_* A hack is what it is ... I suppose the search functions can be relocated elsewhere
	
	def dump_out(self):
		self.report("Dump Out")
		
		return self.root.contents
	
	def dump_in(self, item_list):
		self.report("Dump In")
	
		self.root.contents=item_list
		
	#--
		
	def save(self, file_name):
		#Prepare item data for storage
		data=self.root
		self.db.save(file_name, data)
		

	def load(self, file_name):
		self.report("Load file "+file_name)
		#load a file
		self.root=self.db.load(file_name)
		
	def add_item(self, parent, model="", contents=None,  description="", quantity=0):
		#
		i=item(parent, model, contents, description ,quantity)
		
		self.report("Added item "+str(item))
		return i
	

		
	def has_item(self, item):
		for i in self.root.contents:
			if i==item:
				return True
		return False
		
	def remove_item(self, item):
		print self.root.contents
	
		try:		
			self.root.contents.remove(item)

		except:
			print "BlancDB_Manager(): Error, cannot remove non-existent object"
			pass
		
""" BlancDB_Writer():
	Writes the item data to a file and reads it back
"""
class BlancDB_Writer():
	def report(self, text):
		print "BlancDB_Writer(): "+str(text)
		
			
	def load(self, file_name):
		input_file = open(file_name, 'rb')
		
		self.data=None	
		
		try:
			self.data = cPickle.load(input_file)
			self.report("Load - `"+str(self.data)+"`")
		except EOFError:
			self.report("EOF ?, perhaps no data, or file.")
			pass

		input_file.close()
		return self.data
		


	def save(self, file_name, data):
		output = open(file_name, 'wb')
		self.report("Save, `"+str(data)+"`")

		# Pickle dictionary using protocol 0.

		cPickle.dump(data, output)
		output.close()

class BlancCSV():
	def report(self, text):
		print "BlancCSV(): "+str(text)
		
	def load(self, filename):
		data=[]
		with open(filename, 'rb') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='\"')
			for row in spamreader:
				data.append(row)
	
		return data
		
	def write_row(self, writer, i):
		data=[i.model, i.manufacturer, i.description, i.quantity, str('%.2f' %i.cost), i.location]
		writer.writerow(data)
		
	def save_dump(self, writer, data, recursive):
		defered=[]
	
		for i in data.contents:
			if not i.is_category():
				print "exporting "+str(i)
				self.write_row(writer, i)
				
			if i.is_category() and recursive:
				defered.append(i)
				self.save_dump(writer, i, recursive)
				continue		
				
		for i in defered:
			self.save_dump(writer, i, recursive)					

		
	def save(self, filename, data, recursive):
		print "file: "+filename
		
		with open(filename, 'wb') as csvfile:
			writer = csv.writer(csvfile, delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
			
			#potentially recursive data dumping function (to CSV)
			self.save_dump(writer, data, recursive)
				

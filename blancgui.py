#!/usr/bin/env python

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

import os
import datetime
import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
import pango

import data

# Check for new pygtk: this is new class in PyGtk 2.4
if gtk.pygtk_version < (2,3,90):
	print "PyGtk 2.3.90 or later required"
	raise SystemExit
	

 
class BlancPrint:
	def __init__(self, content_store, recursive=True):
		window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		window.set_title("Drawing Area Example")
		window.connect("destroy", lambda w: gtk.main_quit())
		self.area = gtk.DrawingArea()
		self.area.set_size_request(400, 300)
		window.add(self.area)
		
		self.content_store=content_store
		self.recursive=recursive
		self.counter=0
		
		self.lines_per_page=60
 
		self.area.connect("expose-event", self.area_expose_cb)
		#self.area.show()
		#window.show()
		self.do_print()
 
	def area_expose_cb(self, area, event):
		self.style = self.area.get_style()
		self.gc = self.style.fg_gc[gtk.STATE_NORMAL]
		self.draw_text()
		return True
		
	def liststore_len(self, liststore):
		itr = liststore.get_iter_first()
	
		i=0
		while itr:
			i+=1
			#continue to next itr
			itr = liststore.iter_next( itr )
		return i
 
	def do_print(self):
		print_op = gtk.PrintOperation()
		
		print self.liststore_len(self.content_store)
		j=1+int(self.liststore_len(self.content_store)/self.lines_per_page)
		print "J IS "+str(j)
		
		print_op.set_n_pages(j)
		print_op.connect("draw_page", self.print_text)
		res = print_op.run(gtk.PRINT_OPERATION_ACTION_PRINT_DIALOG, None)
 
	def draw_text(self):
		self.pangolayout = self.area.create_pango_layout("")

		self.format_text()
		self.area.window.draw_layout(self.gc, 10, 10, self.pangolayout)
		return
 
	def print_text(self, operation=None, context=None, page_nr=None):
		print "PRINT TEXT CALLED"
		self.pangolayout = context.create_pango_layout()
		self.format_text()
		cairo_context = context.get_cairo_context()
		cairo_context.show_layout(self.pangolayout)
		return
		"""
	def dump_text(self, category):
		abscounter=0
		tmpcounter=0
		text=""
		if len(category.contents)>0:
			for i in category.contents:
				abscounter=abscounter+1
				
				if abscounter<self.counter:
					continue
				
				tmpcounter=tmpcounter+1
				
				if tmpcounter>=55:
					self.counter=self.counter+tmpcounter
					break
				
				if i.is_category() and self.recursive:
					text=text+self.dump_text(i)
					continue
					
				text=text+str(i.model).ljust(16)[:16]+" "
				text=text+str(i.manufacturer).ljust(16)[:16]+" "
				text=text+str(i.description).ljust(28)[:28]+" "
				text=text+str(i.quantity).ljust(6)[:6]+" "
				text=text+str(i.cost).ljust(8)[:8]+" "
				text=text+str(i.location).ljust(8)[:8]
				text=text+"\r\n"
		return text
"""
	def dump_text(self, content_store):
		text=""
		
		itr = content_store.get_iter_first()
		abscounter=0
		tmpcounter=0
		while itr:
			abscounter=abscounter+1
			
			if abscounter<self.counter:
				itr = content_store.iter_next( itr )
				continue
			
			tmpcounter=tmpcounter+1
			
			if tmpcounter>=self.lines_per_page:
				self.counter=self.counter+tmpcounter
				break
			
			#get current itrs path
			path=content_store.get_path(itr)
			
			if path:#path could be null?
				i=content_store[path][0]
				text=text+str(i.parent.model).ljust(12)[:12]+" "
				text=text+str(i.model).ljust(12)[:12]+" "
				text=text+str(i.manufacturer).ljust(12)[:12]+" "
				text=text+str(i.description).ljust(28)[:28]+" "
				text=text+str(i.quantity).ljust(6)[:6]+" "
				text=text+str(i.cost).ljust(8)[:8]+" "
				text=text+str(i.location).ljust(8)[:8]
				text=text+"\r\n"
			#continue to next itr
			itr = content_store.iter_next( itr )
		
		return text

	def format_text(self):
		#ie. '10:36AM on July 23, 2010'
		datestring=datetime.datetime.now().strftime("%I:%M%P on %B %d, %Y")
		blanc="BlancIMS V1.0"
		#text="Category: "+self.category.model+" - "+datestring+" - "+blanc+"\r\n"
		text=datestring+" - "+blanc+"\r\n"
		text=text+"____________________________________________________________________________________________\r\n"
		#86 Char Max @ 11 mono font
		text=text+"Category".ljust(12)[:12]+" "
		text=text+"Model".ljust(12)[:12]+" "
		text=text+"Manufacturer".ljust(12)[:12]+" "
		text=text+"Description".ljust(28)[:28]+" "
		text=text+"Qty.".ljust(6)[:6]+" "
		text=text+"Cost".ljust(8)[:8]+" "
		text=text+"Location".ljust(8)[:8]
		text=text+"\r\n\r\n"
		
		text=text+self.dump_text(self.content_store)
		
		#Footer
		text=text+"____________________________________________________________________________________________\r\n"

		self.pangolayout.set_text(unicode(text, "latin-1"))
	   	desc = pango.FontDescription("mono 10")
		self.pangolayout.set_font_description(desc)

class glade_about_window():
	def __init__(self):
		self.builder = gtk.Builder()
		self.builder.add_from_file("./data/about.glade")
		
		self.handlers = {
			"onDeleteWindow": self.quit,
			"gtk_main_quit": self.quit,
			"aboutdialog1_close_cb": self.quit,
			"quit": self.quit
		}
		self.builder.connect_signals(self.handlers)

		self.window = self.builder.get_object("aboutdialog1")
		self.window.show_all()

		self.window.run()
		
	def quit(self, item, item2):
		print "about dialog closing"
		self.window.destroy()
		#gtk.main_quit()
		
class glade_search_window():
	def __init__(self, category):
		self.builder = gtk.Builder()
		self.builder.add_from_file("./data/search.glade")
		
		self.handlers = {
			"onDeleteWindow": self.quit,
			"gtk_main_quit": self.quit,
			"aboutdialog1_close_cb": self.quit,
			"quit": self.quit,
			
			'response':self.response,
			'recursive':self.recursive,
			'case':self.case,
			'quantity':self.quantity,
			'description':self.description,
			'manufacturer':self.manufacturer,
			'model':self.model,
			'cost':self.cost,
			'location':self.location
		}
		

		self.builder.connect_signals(self.handlers)
		
		self.tquery=self.builder.get_object("query")
		self.query=""
		self.model=True
		self.manufacturer=False
		self.description=False
		self.quantity=False
		self.cost=False
		self.location=False
		self.recursive=True

		self.category= self.builder.get_object("label_category")
		self.window = self.builder.get_object("dialog1")
		self.window.show_all()
		
		self.set_category(category)
		self.window.run()
		
	def set_category(self, new_text):
		if new_text and new_text!="":
			new_text='<span weight="bold"> '+new_text+" </span>"
			self.category.set_use_markup(True)
			self.category.set_markup(new_text)
	
	def get_query(self):
		return self.query
		
	def response(self, widget, response_id):
		if response_id==1:
			self.query=self.tquery.get_text()
			print "search dialog: '"+self.query+"'"
		self.quit(None)
		
	def recursive(self, widget):
		self.recursive=not self.recursive
	def case(self, widget):
		self.case=not slef.case
	def quantity(self, widget):
		self.quantity=not self.quantity
	def description(self, widget):
		self.description=not self.description
	def manufacturer(self, widget):
		self.manufacturer=not self.manufacturer
	def model(self, widget):
		print "search model change"
		self.model=not self.model
	def cost(self, widget):
		print "search cost change"
		self.cost=not self.cost
	def location(self, widget):
		self.location=not self.location
		
	def quit(self, item):
		print "search dialog closing"
		self.window.destroy()

class glade_cquit():
	def __init__(self):
		self.report("Created")
		
		self.builder = gtk.Builder()
		self.builder.add_from_file("./data/cquit.glade")
		
		self.handlers = {
			"onDeleteWindow": self.quit,
			"gtk_main_quit": self.quit,
			"response": self.action,
		}
		self.builder.connect_signals(self.handlers)

		self.state=0

		self.window = self.builder.get_object("dialog1")
		self.window.show_all()
				
		self.window.run()
	
		
		
	def report(self, text):
		print "glade_cquit(): "+text
		
	def get_state(self):
		self.report("get_stat()")
		
		self.window.destroy()
		return self.state
		
	def action(self, widget, response_id):
		self.report("action() (response) "+str(response_id))

		self.state=response_id
		
		self.window.destroy()
		
	def quit(self, item, item2):
		self.report("quit()")
		self.window.destroy()	
		
class glade_csave():
	def __init__(self):
		self.report("Created")
		
		self.builder = gtk.Builder()
		self.builder.add_from_file("./data/csave.glade")
		
		self.handlers = {
			"onDeleteWindow": self.quit,
			"gtk_main_quit": self.quit,
			"response": self.action,
		}
		self.builder.connect_signals(self.handlers)

		self.state=0

		self.window = self.builder.get_object("dialog1")
		self.window.show_all()
				
		self.window.run()
	
		
		
	def report(self, text):
		print "glade_csave(): "+text
		
	def get_state(self):
		self.report("get_stat()")
		
		self.window.destroy()
		return self.state
		
	def action(self, widget, response_id):
		self.report("action() (response) "+str(response_id))

		self.state=response_id
		
		self.window.destroy()
		
	def quit(self, item, item2):
		self.report("quit()")
		self.window.destroy()
		
		
		
		
class glade_open_window():
	def __init__(self):
		self.report("Created")
		
		self.builder = gtk.Builder()
		self.builder.add_from_file("./data/open.glade")
		
		self.handlers = {
			"onDeleteWindow": self.quit,
			"gtk_main_quit": self.quit,
			"action": self.action,
		}
		self.builder.connect_signals(self.handlers)

		self.window = self.builder.get_object("open_dialog")
		self.window.show_all()
		
		#set dialog folder
		pathname=os.path.realpath("./examples")
		self.window.set_current_folder(pathname)
		
		self.selection=""
		
		
		filter_database = gtk.FileFilter()
		filter_database.set_name("Database Files (*.bdd)")
		filter_database.add_pattern("*.bdd")
		filter_database.add_pattern("*.BDD")
		
		filter_all = gtk.FileFilter()
		filter_all.set_name("All Files")
		filter_all.add_pattern("*")
		
		self.window.add_filter(filter_database)
		self.window.add_filter(filter_all)
		
		
		self.window.run()
		
		
	def report(self, text):
		print "glade_open_window(): "+text
		
	def get_selection(self):
		self.report("get_selection()")
		
		self.window.destroy()
		return self.selection
		
	def action(self, widget, response_id=1):
		self.report("action() (response)")
		
		if response_id==1:
			self.selection=self.window.get_filename()
		
		self.window.destroy()
		
	def quit(self, item, item2):
		self.report("quit()")
		
		self.window.destroy()



class glade_import_window():
	def __init__(self):
		self.report("Created")
		
		self.builder = gtk.Builder()
		self.builder.add_from_file("./data/open.glade")
		
		self.handlers = {
			"onDeleteWindow": self.quit,
			"gtk_main_quit": self.quit,
			"action": self.action,
		}
		self.builder.connect_signals(self.handlers)

		self.window = self.builder.get_object("open_dialog")
		self.window.show_all()

		#set dialog folder
		pathname=os.path.realpath("./examples")
		self.window.set_current_folder(pathname)
		
		self.selection=""
		
		
		filter_database = gtk.FileFilter()
		filter_database.set_name("CSV Files (*.csv)")
		filter_database.add_pattern("*.csv")
		filter_database.add_pattern("*.CSV")
		
		filter_all = gtk.FileFilter()
		filter_all.set_name("All Files")
		filter_all.add_pattern("*")
		
		self.window.add_filter(filter_database)
		self.window.add_filter(filter_all)
		
		
		self.window.run()
		
		
	def report(self, text):
		print "glade_open_window(): "+text
		
	def get_selection(self):
		self.report("get_selection()")
		
		self.window.destroy()
		return self.selection
		
	def action(self, widget, response_id=1):
		self.report("action() (response)")
		
		if response_id==1:
			self.selection=self.window.get_filename()
		
		self.window.destroy()
		
	def quit(self, item, item2):
		self.report("quit()")
		
		self.window.destroy()


		
class glade_save_window():
	def __init__(self):
		self.report("Created")
		
		self.builder = gtk.Builder()
		self.builder.add_from_file("./data/save.glade")
		
		self.handlers = {
			"onDeleteWindow": self.quit,
			"gtk_main_quit": self.quit,
			"action": self.action,
		}
		self.builder.connect_signals(self.handlers)

		self.window = self.builder.get_object("save_dialog")
		self.window.show_all()
		
		#set dialog folder
		pathname=os.path.realpath("./examples")
		self.window.set_current_folder(pathname)
		
		self.selection=""
		self.filter="database"
		
		
		
		filter_database = gtk.FileFilter()
		self.filter_database=filter_database
		
		filter_database.set_name("Database Files (*.bdd)")
		filter_database.add_pattern("*.bdd")
		filter_database.add_pattern("*.BDD")
		
		filter_all = gtk.FileFilter()
		self.filter_all=filter_all
		
		filter_all.set_name("All Files")
		filter_all.add_pattern("*")
		
		self.window.add_filter(filter_database)
		self.window.add_filter(filter_all)
		
		
		self.window.run()
		
		
	def report(self, text):
		print "glade_save_window(): "+text
		
	def get_selection(self):
		self.report("get_selection()")
		
		self.window.destroy()
		return self.selection
	
	#returns either "database" or "all"
	def get_filter(self):
		self.report("get_filter()")
		
		self.window.destroy()
		return self.filter
		
	def action(self, widget, response_id=1):
		self.report("action() (response)")
		
		if response_id==1:
			self.selection=self.window.get_filename()
			if self.window.get_filter()==self.filter_database:
				self.filter="database"
			else:
				self.filter="all"
		
		self.window.destroy()
		
	def quit(self, item, item2):
		self.report("quit()")
		
		self.window.destroy()

		
class glade_export_window():
	def __init__(self):
		self.report("Created")
		
		self.builder = gtk.Builder()
		self.builder.add_from_file("./data/save.glade")
		
		self.handlers = {
			"onDeleteWindow": self.quit,
			"gtk_main_quit": self.quit,
			"action": self.action,
		}
		self.builder.connect_signals(self.handlers)

		self.window = self.builder.get_object("save_dialog")
		self.window.show_all()
		
		#set dialog folder
		pathname=os.path.realpath("./examples")
		self.window.set_current_folder(pathname)
		
		self.selection=""
		self.filter="csv"
		
		
		
		filter_database = gtk.FileFilter()
		self.filter_database=filter_database
		
		filter_database.set_name("CSV Files (*.csv)")
		filter_database.add_pattern("*.csv")
		filter_database.add_pattern("*.CSV")
		
		filter_all = gtk.FileFilter()
		self.filter_all=filter_all
		
		filter_all.set_name("All Files")
		filter_all.add_pattern("*")
		
		self.window.add_filter(filter_database)
		self.window.add_filter(filter_all)
		
		
		self.window.run()
		
		
	def report(self, text):
		print "glade_export_window(): "+text
		
	def get_selection(self):
		self.report("get_selection()")
		
		self.window.destroy()
		return self.selection
	
	#returns either "database" or "all"
	def get_filter(self):
		self.report("get_filter()")
		
		self.window.destroy()
		return self.filter
		
	def action(self, widget, response_id=1):
		self.report("action() (response)")
		
		if response_id==1:
			self.selection=self.window.get_filename()
			if self.window.get_filter()==self.filter_database:
				self.filter="csv"
			else:
				self.filter="all"
		
		self.window.destroy()
		
	def quit(self, item, item2):
		self.report("quit()")
		
		self.window.destroy()

class glade_window():
	def __init__(self):
		self.builder = gtk.Builder()
		self.builder.add_from_file("./data/main.glade")
		
		self.handlers = {
			"onDeleteWindow":   self.handle_quit,
			"gtk_main_quit":	self.handle_quit,
			"activate_about":	self.about_window,
			
			"action_search" :	self.handle_search,
			'action_export' :	self.handle_export,
			'action_import' :	self.handle_import,
			
			'item_remove' :	self.remove_item,
			'item_add' :	self.add_item,
			'category_add' :	self.add_category,
			'category_delete' :	self.remove_category,
			
			'view_recursive':	self.handle_recursive,
			
			'action_new' :	self.handle_new,
			'action_save' :	self.handle_save,
			'action_save_as' :	self.handle_save_as,
			'action_open':	self.handle_open,
			'action_delete' :	self.no_handler,
			'action_paste' :	self.no_handler,
			'action_copy' :	self.no_handler,
			'action_cut' :	self.no_handler,
			'action_print':	self.handle_print,
			'action_quit' :	self.handle_quit,
			
		}
		self.builder.connect_signals(self.handlers)
		
		self.db=data.BlancDB_Manager()
		self.csv=data.BlancCSV()
		self.file_name=""
		
		#Trees
		self.__init_category_tree__()
		self.__init_content_tree__()

		self.window = self.builder.get_object("window1")
		self.window.connect("delete-event", self.handle_quit, None)
		self.window.show_all()
		
		self.init_new()

		gtk.main()
		
	def init_new(self):	
		self.db.clear()
		self.category_store.clear()
		self.content_store.clear()
		
		self.filename=""
		self.category_selected=self.db.root
		self.view_recursive=True
		
		parent=self.db.root
		self.category_store.append(None, [parent, parent.model])
	
	def report(self, text):
		#
		print "glade_window(): "+str(text)
		
	def handle_quit(self, foo=None, bar=None, baz=None):
		#Prompt if the user wants to save before quitting and or continue
		dialog=glade_cquit()
		
		
		#if 1 aka 'yes", then save and quit
		if dialog.get_state()==1:
			self.handle_save(data)
		#if 0 aka "no", just quit
			
		gtk.main_quit()
			
		
		
	def filename_is_valid(self, filename):
		self.report("filename_is_valid, "+str(filename))
	
		if not filename==None and not str(filename)=="" and not os.path.isdir(str(filename)):
			self.report("filename_is_valid, True")
			return True
		self.report("filename_is_valid, False")
		return False
	
	#Prompt:
	# "The database has been modified, would you like to save changes ?"
	#Returns:
	# True - Continue and potentially start new
	# False - Do Not Continue, *do not make any changes !*
	
	def confirm_changes(self):
		dialog=glade_csave()
		
		#if 0 aka "cancel", then return
		if dialog.get_state()==0:
			return False
			
		#if 2 aka 'yes", then save
		if dialog.get_state()==2:
			self.handle_save(data)
			
		#if 1 aka "no",  then pass
		return True
		
	def handle_new(self, data):
		self.report("handle_new")
		
		#Prompt if the user wants to save and or continue
		#(function handles saving)
		#If they wish to continue, start a new database
		if self.confirm_changes():
			self.init_new()		
		
		
	def handle_save(self, data1):
		self.report("handle_save")
		
		if self.filename_is_valid(self.file_name):
			self.save_db(self.file_name)
		else:
			#Hey, This is potenial for an infinite loop if Save as gets broken and passes ""
			self.handle_save_as(None)
			
	def append_file_type(self, ftype, name):
		#if its a database file and doesn't contain the file extension
		# append it
		if ftype=="database" and name.find(".bdd")==-1 and name.find(".BDD")==-1:
			name=name+".bdd"
			
		if ftype=="csv" and name.find(".csv")==-1 and name.find(".CSV")==-1:
			name=name+".csv"
			
		return name
		
	def handle_save_as(self, data1):
		self.report("handle_save_as")
		
		dialog=glade_save_window()
		selection=dialog.get_selection()
		ftype=dialog.get_filter()
		
		if self.filename_is_valid(selection):
			self.file_name=self.append_file_type(ftype, str(selection))
			self.handle_save(None)
		
	def handle_open(self, widget):
		self.report("handle_open")
		
		dialog=glade_open_window()
		selection=dialog.get_selection()
		
		if self.filename_is_valid(selection):
			self.file_name=str(selection)
			self.load_db(self.file_name)
			
	def handle_export(self, widget):
		self.report("handle_export")
		
		dialog=glade_export_window()
		selection=dialog.get_selection()
		ftype=dialog.get_filter()
		
		if self.filename_is_valid(selection):
			filename=self.append_file_type(ftype, str(selection))
			self.export_category(filename, self.category_selected)
	
	def handle_import(self, widget):
		self.report("handle_import")
		
		dialog=glade_import_window()
		filename=dialog.get_selection()
		
		if self.filename_is_valid(filename):
			self.import_category(filename, self.category_selected)
			
	def handle_search(self, widget):
		print self.category_selected
		if self.category_selected==None:
			self.report("handle_search, no category")
			searchw=glade_search_window(None)
		else:
			self.report("handle_search,")
			searchw=glade_search_window(str(self.category_selected.model))
		
		query=searchw.get_query()
		print "Got query of "+query
		
		if query!="":
			self.search(self.category_selected, query,
				searchw.model, searchw.manufacturer, searchw.description,
				searchw.quantity, searchw.case, searchw.recursive,
				searchw.cost, searchw.location)
		
		return
		
	def handle_print(self, widget):
		#BlancPrint(self.category_selected, self.view_recursive)
		BlancPrint(self.content_store, self.view_recursive)
		
	def handle_recursive(self, widget):
		self.view_recursive=not self.view_recursive
		self.category_select(self.category_selected)
					
	#----
	def load_category(self, item):
		#Assume that item provied is a category
		#add category
		#
		#Go through all items looking for categories
		# if category Call this
		
		
		
		itr = self.category_store.get_iter_first()	 #
		print "Piner= "+str(itr)
		parent_category=self.compare_children(self.category_store, item.parent, itr)
		print "Found "+str(parent_category)
		
		print "Iterable Hunt"
		while itr:
		
			path=self.category_store.get_path(itr)
			print path
			print self.category_store[path][0]
			itr=self.category_store.iter_next( itr )
		print "Finish"
		
		self.report("load_category, adding category "+item.model+ " to parent "+str(parent_category))
		self.category_store.append(parent_category, [item, item.model])
		
		for i in item.contents:
			if i.is_category():
				#call this function to add its childern
				self.load_category(i)
			
			
			
	def load_db(self, filename):	
		self.report("load_db, "+filename)
		
		#Load new Database
		self.db.load(filename)
		
		#Clear Window
		self.content_store.clear()
		self.category_store.clear()
		
		#Add root category
		#parent=self.db.root
		#self.category_store.append(None, [parent, parent.model])
		
		#Go through every category
		self.load_category(self.db.root)
		
		self.category_select(self.db.root)
		
	def save_db(self, filename):
		self.report("save_db, "+filename)
		
		self.db.save(filename)
		
	def export_category(self, filename, category):
		self.csv.save(filename, category, self.view_recursive)
		
	def import_category(self, filename ,category):
		dat=self.csv.load(filename)
		
		#ncat=data.item(parent=category,model="Default", contents=[])
		for row in dat:
			print row
			#not ncat but cat
			#hack to prevent import from creating a new category
			data.item(parent=category, model=row[0], manufacturer=row[1], description=row[2], quantity=row[3], cost=row[4], location=row[5])
			
		#self.add_category_parent( category, ncat)
		#not ncat but cat
		self.category_select(category)
		
	def __init_category_tree__(self):
		self.tree_category = self.builder.get_object("tree-category")

		# set model (i.e. the data it contains. We assume this is not done via glade.)
		self.category_store = gtk.TreeStore(object, str)
		self.tree_category.set_model(self.category_store)
		
		self.tree_category.connect("cursor-changed", self.category_select_cursor)

		# add columns:
		#cell0 = gtk.CellRendererText()
		#col0 = gtk.TreeViewColumn("ID", cell0, text=0)
		#self.tree_category.append_column(col0)
		
		# add columns:
		cell1 = gtk.CellRendererText()
		cell1.set_property( 'editable', True )
		
		cell1.connect( 'edited', self.category_edited, self.category_store)
		
		col1 = gtk.TreeViewColumn("Category", cell1, text=1)
		#col1.set_resizable(True)
		self.tree_category.append_column(col1)
	
	def __init_content_tree__(self):
		self.tree_content = self.builder.get_object("tree-content")
		

		# set model (i.e. the data it contains. We assume this is not done via glade.)
		
		#ID, category, model, manufacturer, description, quantity, cost, Location
		self.content_store = gtk.ListStore(object, str, str, str, str, int, str, str)
		store=self.content_store
		
		self.tree_content.set_model(store)


		#Don't display blank IDs
		# add  ID column
		#cell0 = gtk.CellRendererText()
		
		#col0 = gtk.TreeViewColumn("ID", cell0, text=0)
		#self.tree_content.append_column(col0)
		
		# add Category column
		cell1 = gtk.CellRendererText()
		
		col1 = gtk.TreeViewColumn("Category", cell1, text=1)
		col1.set_resizable(True)
		self.tree_content.append_column(col1)

		# add Model column
		cell2 = gtk.CellRendererText()
		cell2.set_property( 'editable', True )
		cell2.connect( 'edited', self.content_model_edited, store )
		
		col2 = gtk.TreeViewColumn("Model", cell2, text=2)
		col2.set_resizable(True)
		self.model_column=col2
		
		self.tree_content.append_column(col2)
		
		# add Manufacturer column
		cell3 = gtk.CellRendererText()
		cell3.set_property( 'editable', True )
		cell3.connect( 'edited', self.content_manufacturer_edited, store )
		
		col3 = gtk.TreeViewColumn("Manufacturer", cell3, text=3)
		col3.set_resizable(True)
		self.model_column=col3
		
		self.tree_content.append_column(col3)
		
		# add columns:
		cell4 = gtk.CellRendererText()
		cell4.set_property( 'editable', True )
		cell4.connect( 'edited', self.content_description_edited, store )
		
		col4 = gtk.TreeViewColumn("Description", cell4, text=4)
		col4.set_resizable(True)
		self.tree_content.append_column(col4)
		
		# add columns:
		cell5 = gtk.CellRendererText()
		cell5.set_property( 'editable', True )
		cell5.connect( 'edited', self.content_quantity_edited, store )
		
		col5 = gtk.TreeViewColumn("Quantity", cell5, text=5)
		col5.set_resizable(True)
		self.tree_content.append_column(col5)
		
		# add columns:
		cell6 = gtk.CellRendererText()
		cell6.set_property( 'editable', True )
		cell6.connect( 'edited', self.content_cost_edited, store )
		
		col6 = gtk.TreeViewColumn("Cost", cell6, text=6)
		col6.set_resizable(True)
		self.tree_content.append_column(col6)
		
		# add columns:
		cell7 = gtk.CellRendererText()
		cell7.set_property( 'editable', True )
		cell7.connect( 'edited', self.content_location_edited, store )
		
		col7 = gtk.TreeViewColumn("Location", cell7, text=7)
		col7.set_resizable(True)
		self.tree_content.append_column(col7)
		
		# add columns:
		cell8 = gtk.CellRendererText()
		
		col8 = gtk.TreeViewColumn("", cell8, text=8)
		self.tree_content.append_column(col8)	

	
	def category_edited( self, cell, path, new_text, model ):
		"""
		Called when a text cell is edited. Insert the new_text
		into the Category name so that its displayed properly.
		
		The magic number is the col
		"""

		if self.db.root==model[path][0]:
			#in the event that the user is renaming the ROOT category, the cannot
			print "Cannot Rename Root"
			return
			
		model[path][1] = new_text
		#Set the category name
		#self.db.item_set_model(model[path][0],new_text)
		model[path][0].model=new_text
		
		
		for i in model[path][0].contents:
			i.parent=model[path][0]
			
		self.category_select_cursor(self.tree_category)

		
		
		return
		
	def content_model_edited( self, cell, path, new_text, model ):
		"""
		Called when a text cell is edited.  It puts the new text
		in the model so that it is displayed properly.
		
		The magic number is the col
		"""
		model[path][2] = new_text
		
		model[path][0].model=new_text

		return
		
	
	
	def content_manufacturer_edited( self, cell, path, new_text, model ):
		"""
		Called when a text cell is edited.  It puts the new text
		in the manufacturer so that it is displayed properly.
		
		The magic number is the col
		"""
		model[path][3] = new_text
		
		model[path][0].manufacturer=new_text

		return


	def content_description_edited( self, cell, path, new_text, model ):
		"""
		Called when a text cell is edited.  It puts the new text
		in the model so that it is displayed properly.
		
		The magic number is the col
		"""
		model[path][4] = new_text
		
		model[path][0].description=new_text

		return
	
	def content_quantity_edited( self, cell, path, new_text, model ):
		"""
		Called when a text cell is edited.  It puts the new text
		in the model so that it is displayed properly.
		
		The magic number is the col
		"""
		if new_text.isdigit():
			model[path][5] = int(new_text)
			print "Set Quantity"
			model[path][0].quantity=int(new_text)
		return
		
	def content_cost_edited( self, cell, path, cost, model ):
		"""
		Called when a text cell is edited.  It puts the new text
		in the model so that it is displayed properly.
		
		The magic number is the col
		"""
		model[path][6] = '%.2f' % float(cost)
		print "Set cost"
		model[path][0].cost=float(model[path][6])
		return
		
		
	def content_location_edited( self, cell, path, new_text, model ):
		"""
		Called when a text cell is edited.  It puts the new text
		in the model so that it is displayed properly.
		
		The magic number is the col
		"""
		model[path][7] = new_text
		
		model[path][0].location=new_text
		return
		
	def category_check(self, parent):
		if parent==None:
			return
		
		itr=self.category_store.get_iter_first()
		
		path=None
		while itr:
			path=self.category_store.get_path(itr)
			if path!=None:
				if parent==self.category_store[path][0]:
					return
			
			#was model
			itr = self.category_store.iter_next( itr )
			
		self.category_store.append(None, [parent, parent.model])
		
		
	def get_last(self, model ):
		itr = model.get_iter_first()
		last = None
		while itr:
			last = itr
			itr = model.iter_next( itr )

		return last
		
	def add_item(self, stuff):
		if self.category_selected==None:
			print "add_item, no category selected"
			self.category_selected=self.db.root
	
		print "adding_item, to "+self.category_selected.model	
		
		
		
		item=data.item(parent=self.category_selected, model="Default")
		self.category_select( self.category_selected)
		
		"""
		last=self.get_last(self.content_store)
		path=self.content_store.get_path(last)
		
		self.tree_content.grab_focus()
		self.tree_content.set_cursor(path,self.model_column, True)"""
		
	
	def remove_item(self, stuff):
		
		sel=self.tree_content.get_cursor()[0]
		if sel!=None:
			sel=sel[0]
			item=self.content_store[sel][0]
			
			for row in self.content_store:
				if row[0] == item:
					self.content_store.remove(row.iter)
					item.parent.contents.remove(item)
					print "Removed"
					break


	#recursive function that navigates the entire category structure looking for an (object) match
	#
	#-- Go through the provdied TreeStore and find the iterable of the
	#   entry with the specified object pointer
	#Returns:
	#   Iterable of the object
	
	def compare_children(self, store, item, itr):	
	
		while itr:
			print "\tNext Iter"
			
			#get children in store (if any.) Call this function
			if store.iter_children(itr):
				print "\tChildren"
				child_itr=store.iter_children(itr)
				result=self.compare_children(store, item, child_itr)
				#if we got a match, (not None) return
				if result:
					print "iter found"
					return result
			
			#get current itrs path
			path=store.get_path(itr)
			print path
			if path:#path could be null?
				#resolve path to desired object and compare to desired
				if item==store[path][0]:
					#match: return its iterable
					print "iter found"
					return itr
				else:
					print "iter not same"
			else:
				print "\titer is null"
				
			#no match: continue to next itr at the level
			itr = store.iter_next( itr )
			
		#failure no more Iters left, return None
		print "No iter found."
		return None		

	def add_category(self, widget):		
		
		if not self.category_selected:
			return
			
		itr = self.category_store.get_iter_first()
		parent_category=self.compare_children(self.category_store, self.category_selected, itr)

		item=data.item(parent=self.category_selected, model="Default", contents=[])
		
		self.category_store.append(parent_category, [item, item.model])
		
	def add_category_parent(self, parent, child):
		itr = self.category_store.get_iter_first()
		parent_category=self.compare_children(self.category_store, parent, itr)
		
		self.category_store.append(parent_category, [child, child.model])
		
	def remove_category(self, widget):
		print self.category_selected
		print self.category_selected.model
		print self.category_selected.parent.model
		
		if not self.category_selected:
			return
			
		if self.category_selected==self.db.root:
			return
			
		itr = self.category_store.get_iter_first()
		category_iter=self.compare_children(self.category_store, self.category_selected, itr)
		
		parent=self.category_selected.parent
		
		#remove the category from its parent in the database
		self.category_selected.parent.contents.remove(self.category_selected)

		#Remove from the category list
		self.category_store.remove(category_iter)
		
		#select the parent category
		self.category_select( parent)
		
	#now the only function dealing with adding new items to gui !
	#far easier to add new coulums now,
	def add_i_to_content(self, i):
		#Add item into GUI content
		self.content_store.append([i, i.get_category(),
			i.model, i.manufacturer, i.description,
			i.quantity, '%.2f' %i.cost, i.location])
			
			
	#recursive category display function
	def category_dump(self, category):
		
		defered=[]
		
		for i in category.contents:
			#reverse normal order to make selected category contents display above subcategory contents
			if not i.is_category():
				#Add to content
				self.add_i_to_content(i)
			else:
				if self.view_recursive:
					defered.append(i)

		for i in defered:
			self.category_dump(i)
			
		
				
	#change category to category and repopulate the content field
	def category_select(self, category):
		self.report("category_select, "+category.model)
		self.category_selected=category
		
		self.content_store.clear()
		
		self.category_dump(category)
			
		
	def category_select_cursor(self,category_tree):
		#returns a tuple, model and path
		path=category_tree.get_cursor()
		#extract path
		path=path[0]
		
		#path may be NULL
		if path:
			self.category_selected=self.category_store[path][0]
		
		self.report("category_select_cursor, "+self.category_selected.model)
		
		self.content_store.clear()
		
		self.category_dump(self.category_selected)
	
	def search(self, category, query,
			model=True, manufacturer=False, description=False,
			quantity=False, case=False, recursive=False,
			cost=False, location=False):
		
		if query=="":
			print "Search Aborted nothing"
			return
			
		if not category:
			print "Search Aborted category null"
			return
			
		if category.contents==None:
			print "Search Aborted none"
			return
			
		if len(category.contents)==0:
			print "Search Aborted 0"
			return
		#do search-esque stuff

		
		results=[]
		
		if model:
			results=results+self.search_model( category, query, case, recursive)
		
		if manufacturer:
			results=results+self.search_manufacturer( category, query, case, recursive)

		if description:
			results=results+self.search_description( category, query, case, recursive)

		if quantity:
			results=results+self.search_quantity( category, query, case, recursive)	
				
		if cost:
			results=results+self.search_cost( category, query, case, recursive)	
			
		if location:
			results=results+self.search_location( category, query, case, recursive)	
			
		self.content_store.clear()
		
		for i in list(set(results)):
			#add i to GUI content field
			self.add_i_to_content(i)
			
			
	#devnote: case disregarded
	def search_model(self, category, query, case, recursive):
		if query=="":
			print "Search Model Aborted nothing"
			return []
			
		if not category:
			print "Search Model Aborted category null"
			return
			
		if category.contents==None:
			print "Search Model Aborted none"
			return []
			
		if len(category.contents)==0:
			print "Search Model Aborted 0"
			return []
	
		results=[]
		for i in category.contents:
			print i.model
			
			if i==category:
				print "search_model, ERROR category contains itself !"
				continue
			
			if recursive and i.is_category():
				results=results+self.search_model( i, query, case, recursive)
				continue
				
			search_model=i.model.lower()
			search_term=query.lower()
			if search_model.find(search_term)!=-1:
				results=results+[i]
				
		return results
	
	#devnote: case disregarded
	def search_manufacturer(self, category, query, case, recursive):
		if query=="":
			print "Search Model Aborted nothing"
			return []
			
		if not category:
			print "Search Model Aborted category null"
			return
			
		if category.contents==None:
			print "Search Model Aborted none"
			return []
			
		if len(category.contents)==0:
			print "Search Model Aborted 0"
			return []
	
		results=[]
		for i in category.contents:
			print i.model
			
			if i==category:
				print "search_model, ERROR category contains itself !"
				continue
			
			if recursive and i.is_category():
				results=results+self.search_manufacturer( i, query, case, recursive)
				continue
				
			search_model=i.manufacturer.lower()
			search_term=query.lower()
			if search_model.find(search_term)!=-1:
				results=results+[i]
		return results
		

	#devnote: case disregarded
	def search_description(self, category, query, case, recursive):
		if query=="":
			print "Search Model Aborted nothing"
			return []
			
		if not category:
			print "Search Model Aborted category null"
			return
			
		if category.contents==None:
			print "Search Model Aborted none"
			return []
			
		if len(category.contents)==0:
			print "Search Model Aborted 0"
			return []
	
		results=[]
		for i in category.contents:
			print i.model
			
			if i==category:
				print "search_model, ERROR category contains itself !"
				continue
			
			if recursive and i.is_category():
				results=results+self.search_description( i, query, case, recursive)
				continue
				
			search_description=i.description.lower()
			search_term=query.lower()
			if search_description.find(search_term)!=-1:
				results=results+[i]
				
		return results
	
	
	#devnote: case disregarded
	def search_quantity(self, category, query, case, recursive):
		if query=="":
			print "Search Model Aborted nothing"
			return []
			
		if not category:
			print "Search Model Aborted category null"
			return
			
		if category.contents==None:
			print "Search Model Aborted none"
			return []
			
		if len(category.contents)==0:
			print "Search Model Aborted 0"
			return []
	
		results=[]
		for i in category.contents:
			print i.model
			
			if i==category:
				print "search_model, ERROR category contains itself !"
				continue
			
			if recursive and i.is_category():
				results=results+self.search_quantity( i, query, case, recursive)
				continue
				
			search_quantity=str(i.quantity)
			search_term=query
			if search_quantity.find(search_term)!=-1:
				results=results+[i]
				
		return results
	
#devnote: case disregarded
	def search_cost(self, category, query, case, recursive):
		if query=="":
			print "Search Model Aborted nothing"
			return []
			
		if not category:
			print "Search Model Aborted category null"
			return
			
		if category.contents==None:
			print "Search Model Aborted none"
			return []
			
		if len(category.contents)==0:
			print "Search Model Aborted 0"
			return []
	
		results=[]
		for i in category.contents:
			
			if i==category:
				print "search_model, ERROR category contains itself !"
				continue
			
			if recursive and i.is_category():
				results=results+self.search_cost( i, query, case, recursive)
				continue
				
			search_cost=str(i.cost)
			search_term=query
			if search_cost.find(search_term)!=-1:
				results=results+[i]
				
		return results
	
	
#devnote: case disregarded
	def search_location(self, category, query, case, recursive):
		if query=="":
			print "Search Model Aborted nothing"
			return []
			
		if not category:
			print "Search Model Aborted category null"
			return
			
		if category.contents==None:
			print "Search Model Aborted none"
			return []
			
		if len(category.contents)==0:
			print "Search Model Aborted 0"
			return []
	
		results=[]
		for i in category.contents:
			
			if i==category:
				print "search_model, ERROR category contains itself !"
				continue
			
			if recursive and i.is_category():
				results=results+self.search_location( i, query, case, recursive)
				continue
				
			search_location=str(i.location)
			search_term=query
			if search_location.find(search_term)!=-1:
				results=results+[i]
				
		return results
	
	def about_window(self, item):
		print "about"
		glade_about_window()
		
	def no_handler(self, data):
		print data
		
		return
		
if __name__=="__main__":
	glade_window()

#!/usr/bin/python
from data import *

		
def add_item(db):
	name=str(raw_input('Model: '))
	desc=str(raw_input('Desc: '))
	qty=int(raw_input('Qty: '))
	db.add_item(name, desc, qty)
	
def save(db):
	name=str(raw_input('Enter DB File Name: '))
	db.save(name)
	
	for i in db.dump_out():
		print "Item: "+str(i)+", "+str(i.model)+", "+str(i.description)+", "+str(i.quantity)
	print "Saved as `"+name+"`"
	
#--------------------------------------------
		

print "Welcome to DB Manager"
db=BlancDB_Manager()		
while 1:
	print "Menu:"
	print " 1: Add"
	print " 2: Save"
	
	cmd=str(raw_input('Enter Command: '))
	if cmd=="1":
		add_item(db)
	if cmd=="2":
		save(db)
		
	

	
"""


db.add_item("B", 10, "Model B desc.")
db.add_item("AA", 10, "Model AA desc.")
db.add_item("AB", 10, "Model AB desc.")
db.add_item("PIC16F690-I/A", 10, "Model PIC16F160-I/a desc.")


print ""
print "Searching ! A"
for i in db.contains_description("A"):
	print i"""

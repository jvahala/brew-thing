import string
import objects
import numpy as np

class Parser(object): 
	def __init__(self,column_names): 
		self.column_names = column_names	#list of column names

class HopParser(Parser): 
	def __init__(self,column_names,style): 
		#super().__init__(column_names)
		self.column_names = column_names
		self.style = style

	def parse(self,table): 
		#parses the data table into a new table self.parsed with elements associated with self.parsed_names
		self.parsed_names = {'Name':0,'Country':1,'Expected Alpha Acid %':2,'Substitutions':3,'Flavors':4}
		self.parsed = np.empty((len(table),len(self.parsed_names)),dtype='object')

		for r,row in enumerate(table):
			print 'row', row
			for c,elt in enumerate(row): 
				 #parse names
				 print 'elt', elt
				 if 'name' in self.column_names[c].lower():
				 	test = elt.rpartition(' (')[0]
				 	print self.parsed_names['Name']
				 	if test == '': 
				 		self.parsed[r,self.parsed_names['Name']] = elt		#name
				 		self.parsed[r,self.parsed_names['Country']] = 'n/a'	#country
				 	else: 
				 		self.parsed[r,self.parsed_names['Name']] = test 	#name
				 		self.parsed[r,self.parsed_names['Country']] = elt.partition('(')[-1].rpartition(')')[0]	#country
				 
				 #parse alpha acid percentage
				 elif 'acid' in self.column_names[c].lower(): 
				 	print self.parsed_names['Expected Alpha Acid %'], elt
				 	if elt.lower() == 'na': 
				 		self.parsed[r,self.parsed_names['Expected Alpha Acid %']] = 'n/a'
				 		continue
				 	test = elt.rpartition('-')[0]
				 	if test == '': 		#no bounds, take everything but percent as expected AA%
				 		if elt.rpartition('%')[0] == '': 		#if no '%' sign (should never happen), just grab the numbers
				 			self.parsed[r,self.parsed_names['Expected Alpha Acid %']] = float(elt)
				 		else: 
				 			self.parsed[r,self.parsed_names['Expected Alpha Acid %']] = float(elt.rpartition('%')[0])
				 	else: 
				 		small = float(test)
				 		large = float(elt.partition('-')[-1].rpartition('%')[0])
				 		self.parsed[r,self.parsed_names['Expected Alpha Acid %']] = (small+large)/2. 	#average value of the extremes 

				 #parse substitutes
				 elif 'subs' in self.column_names[c].lower(): 
				 	if elt == '': 
				 		self.parsed[r,self.parsed_names['Substitutions']] = 'n/a'
				 	else: 
				 		country_names = ['U.K. ', 'U.S. ', 'French ']
				 		subslist = elt.replace('perhaps','').replace('Perhaps','').replace('possibly','').replace('Possibly','').split(',') 	#this can be done better
				 		subslist = [x[1:] if x[0]==' ' else x for x in subslist]
				 		'''need to remove country words'''
				 		self.parsed[r,self.parsed_names['Substitutions']] = subslist

				 elif 'flavor' in self.column_names[c].lower(): 
				 	self.parsed[r,self.parsed_names['Flavors']] = 'n/a'




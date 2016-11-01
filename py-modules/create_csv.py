# -*- coding: utf-8 -*-
'''
create_csv.py
Takes the hopGroup object (a list of hop objects) and parses the hop.advanced_oil_description to create a csv file separated by tabs
'''
import unicodecsv

def defineCsv(hopGroup,filename='mydata.csv',exp_numel=11):
	#find a hop with the exp_numel, the expected number of elements, or just the one with the most numel to base the header on
	choice = findBestNumel(hopGroup,exp_numel)
	header_hop = hopGroup[choice.keys()[0]]
	header_hop_oilLength = choice.values()[0]

	#define header row and unit row
	header_oils,header,units = defineHeaderAndUnitRows(header_hop)

	# gather the details for all hops
	all_details = gatherHopDetails(hopGroup,header,header_oils)	#list of lists with all necessary hop details 
	output_csv_info = [header]+[units]+all_details

	#export to csv file
	writeCsv(output_csv_info,filename)
	return all_details

def findBestNumel(hopGroup,exp_numel):
	max_element_choice = {0:0}		#holds the best choice if the expected number of elements is not found
	for i,hop in enumerate(hopGroup): 
		curr_hop_numel = len(hop.advanced_oil_description)

		if curr_hop_numel > max_element_choice.values()[0]: 
			max_element_choice = {i:curr_hop_numel}
			if curr_hop_numel == exp_numel: 
				return max_element_choice
	return max_element_choice

def defineHeaderAndUnitRows(header_hop):
	header_oils = header_hop.advanced_oil_description.keys()
	header = ['name','url','use','rating','aromas']		#basic things and their units
	units = ['','','','stars','']
	for oil_name in header_oils: 
		header += [oil_name+'-low']
		header += [oil_name+'-mid']
		header += [oil_name+'-high']
		units += [header_hop.advanced_oil_description[oil_name]['unit']]*3
	return header_oils,header,units

def gatherHopDetails(hopGroup,header,header_oils):
	all_details = []
	lowmidhigh = ['lower','middle','upper']
	for hop in hopGroup:
		hop_details = ['']*len(header)

		# fill out basics
		hop_details[0] = hop.name 
		hop_details[1] = hop.url
		hop_details[2] = hop.use
		hop_details[3] = hop.rating
		hop_details[4] = hop.aromas

		k = 5
		for i,oil_name in enumerate(header_oils):
			for j in range(3):
				try: 
					hop_details[k+j] = hop.advanced_oil_description[oil_name][lowmidhigh[j]]
				except KeyError: 
					break
			k = k+3
		all_details += [hop_details]
	return all_details

def writeCsv(inputList,filename='mydata.csv'):
	with open(filename, 'w') as mycsvfile:
		thedatawriter = unicodecsv.writer(mycsvfile)
		for row in inputList:
			thedatawriter.writerow(row)
	print 'data written to '+filename 









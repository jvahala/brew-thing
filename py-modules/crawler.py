# coding: utf-8
import string

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException

import time
import objects
import numpy as np

class Crawler(object): 
	def __init__(self,url,dropdownName):
		self.url = url
		self.driver = webdriver.Chrome()
		self.driver.get(self.url)
		self.names = []
		self.entryIDs = ['sectiontableentry1','sectiontableentry2']
		self.dropdownName = dropdownName
		self.curr_style_val = 1
		self.curr_style_str = ''

	def selectStyle(self,value): 
		#change the page using the dropdown style selector menu

		driver = self.driver
		select = Select(driver.find_element_by_name(self.dropdownName))
		select.select_by_value(str(value))
		self.curr_style_val = value

	def getTableContents(self):

		def getElementNames(soup): 
			names = []
			for header in soup.findAll('td',{'class':'sectiontableheader'}):
				names.append(str(header.string)) 
			return names

		def getElements(soup): 
			element_array = np.empty((1,len(self.names)),dtype='object')
			add_row = element_array
			for eind, elt in enumerate(soup.findAll('tr',{'class':self.entryIDs[0],'class':self.entryIDs[1]})):
				printable = set(string.printable)
				components = len(elt.findAll('td'))
				for iind,item in enumerate(elt.findAll('td')): 
					try: 
						item = filter(lambda x: x in printable, item.string)
					except TypeError: 
						item = ''
					element_array[eind,iind] = str(item).replace('\n','').replace('\t','')
				element_array = np.vstack((element_array,add_row))
			return element_array

		driver = self.driver
		WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_name(self.dropdownName))

		source_code = driver.page_source
		soup = BeautifulSoup(source_code,'lxml')
		curr_style_list = soup.findAll('option',{'value':str(self.curr_style_val)})
		self.curr_style_str = str(curr_style_list[0].string.replace(u'ö','o').replace(u'ü','u'))
		if len(self.names) == 0: 
			self.names = getElementNames(soup)
		output_array = getElements(soup)
		return self.curr_style_str, self.names, output_array

	def endDriver(self):
		self.driver.quit()

def setupCrawler(baseurl,crawl_type):
	if crawl_type[0].lower() == 'h': 		#crawl hops page
		url = baseurl+'hops'
		dropdown = 'style'
	elif crawl_type[0].lower() == 'y': 		#crawl yeast page
		url = baseurl+'yeast'
		dropdown = 'style'
	elif crawl_type[0].lower() == 'g': 		#crawl grains page
		url = baseurl+'grains'
		dropdown = 'gtype'
	else: 
		return '#####ERROR: crawl_type must be \'hops\', \'yeast\', or \'grains\''
	crawler = Crawler(url=url, dropdownName=dropdown)
	return crawler 

def crawlStyle(crawler,style_id,problem_child=0,print_details=False):
	try: 
		crawler.selectStyle(style_id)
		problem_child=0
	except NoSuchElementException: 
		print '\n----------------\n######ERROR: revise styleslist (element ',str(i),' not found)\n----------------\n\n'
		problem_child += 1
		if problem_child > 2:
			print '\n----------------\n######ERROR: problem_child done run a muck. Iteration ended.\n----------------\n\n'

	return crawler,problem_child

def crawlMultiple(baseurl,styleslist,crawl_type):

	#setup crawler url and dropdown selection based on crawl_type
	crawler = setupCrawler(baseurl,crawl_type)
	
	#go through styleslist numbers
	problem_child = 0
	for i in styleslist:
		try: 
			crawler.selectStyle(i)
			problem_child=0
		except NoSuchElementException: 
			print '\n----------------\n######ERROR: revise styleslist (element ',str(i),' not found)\n----------------\n\n'
			problem_child += 1
			if problem_child > 2:
				print '\n----------------\n######ERROR: problem_child done run a muck. Iteration ended.\n----------------\n\n'
				break
			continue

		style, names, output = crawler.getTableContents()

		#print the current page crawl results
		print style, i
		#print names
		#print output
		#print '--------\n\n'

	#terminate the driver connection	
	crawler.endDriver()

	return style, names, output

def main(): 
	#crawl type is either 'hops', 'yeast', or 'grains', styleslist is the list of values associated with the dropdown html options
	baseurl = 'https://byo.com/resources/'
	styleslist = np.arange(28)+1
	crawl_type = 'hops'
	style,names,output = crawlMultiple(baseurl,styleslist=styleslist,crawl_type=crawl_type)
	return style,names,output


if __name__ == '__main__': main()

'''
American Lager 1
American Amber & Pale Ale 2
Barleywine and Imperial Stout 3
Belgian and French Ale 4
Belgian Lambic and Sour Ale 5
Belgian Strong Ale 6
Bock 7
Brown Ale 8
Cider 9
English & Scottish Strong Ale 10
English Bitter & Pale Ale 11
European Dark Lager 12
European Pale Lager 13
Fruit Beer 14
German Amber Lager 15
India Pale Ale 16
Kolsch & Altbier 17
Light Ale 18
Mead 19
Porter 20
Scottish Ale 21
Smoked Beer 22
Soda Pop 23
Specialty & Experimental Beer 24
Spice, Herb & Vegetable Beer 25
Stout 26
Wheat Beer 27
American Pale Ale 28
'''

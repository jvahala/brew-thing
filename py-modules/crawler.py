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
		self.curr_style_str = curr_style_list[0].string.replace(u'ö','o')
		if len(self.names) == 0: 
			self.names = getElementNames(soup)
		output_array = getElements(soup)
		return self.curr_style_str, self.names, output_array

	def endDriver(self):
		self.driver.quit()




if __name__ == '__main__':
	#setup stuff, chose appropriate url and dropdown options for your crawl
    baseurl = 'https://byo.com/resources/'
    hopurl = baseurl+'hops'
    grainurl = baseurl+'grains'
    yeasturl = baseurl+'yeast'
    grain_dropdown = 'gtype'
    hop_yeast_dropdown = 'style'

    #define which styles/values to crawl over (see options in html)
    styleslist = np.arange(28)+1	#in range {1,2,3,...}
    print styleslist

    #choose Crawler class
    #currCrawler = Crawler(url=grainurl,dropdownName=grain_dropdown)
    #currCrawler = Crawler(url=hopurl,dropdownName=hop_yeast_dropdown)
    currCrawler = Crawler(url=yeasturl,dropdownName=hop_yeast_dropdown)

    #iterate through your chosen style numbers
    problem_child = 0
    for i in styleslist:
    	try: 
    		currCrawler.selectStyle(i)
    		problem_child=0
    	except NoSuchElementException: 
    		print '\n----------------\n######ERROR: revise styleslist (element ',str(i),' not found)\n----------------\n\n'
    		problem_child += 1
    		if problem_child > 2:
    			print '\n----------------\n######ERROR: problem_child done run a muck. Iteration ended.\n----------------\n\n'
    			break
    		continue

    	style, names, output = currCrawler.getTableContents()
    	
    	'''here, need to add methods to add information to the database'''

    	#print the current page crawl results
    	print 'CATEGORY: ',style
    	print names
    	print output
    	print '--------\n\n'

    #terminate the driver connection	
    currCrawler.endDriver()


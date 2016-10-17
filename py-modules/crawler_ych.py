# coding: utf-8
'''Crawl https://ychhops.com/varieties for the various aspects associated with an individual hop - oils, aromas, etc'''
import string
import textutils

from bs4 import BeautifulSoup
import urllib
from contextlib import closing

import numpy as np
np.set_printoptions(threshold=np.nan,precision=3,suppress=True)

class Crawler(object): 
	def __init__(self,url): 
		self.url = url 


	def getSoup(self): 
		with closing(urllib.urlopen(self.url)) as sf: 
			self.soup = BeautifulSoup(sf.read(),'lxml')
		#print 'Soup retrieved.'

	def retrieveFromSoup(self,_block=None,_class=None): 
		letters = self.soup.find_all(_block, class_=_class)
		return letters 

	def retrieveAttributes(self,letters,attributes=None):
		if attributes != None: 
			indivs = {}			# indivs = {0: {att1: , att2: , ...}, 1:{}}
			for i,line in enumerate(letters): 
				indivs[i] = {}
				for att in attributes: 
					indivs[i][att] = line[att]
		return indivs


def initialize(url): 
	''' STEP 1 
	init hop group url: "https://ychhops.com/varieties"
	'''

	crawler = None
	crawler = Crawler(url)
	crawler.getSoup()
	return crawler

def getAllTypes(crawler): 
	''' STEP 2 '''
	aromas = getAllHopType(crawler,'aroma')
	bitters = getAllHopType(crawler,'bittering')
	duals = getAllHopType(crawler,'dual')
	return aromas, bitters, duals

def getAllHopType(crawler,hop_type): 
	aroma_div = "col-sm-4 col-lg-3 card blue"
	bitter_div = "col-sm-4 col-lg-3 card red"
	dual_div = "col-sm-4 col-lg-3 card orange"

	hop0 = hop_type[0].lower()
	if hop0 == 'a': 
		letters = crawler.retrieveFromSoup(_block='div',_class=aroma_div)
	elif hop0 == 'b': 
		letters = crawler.retrieveFromSoup(_block='div',_class=bitter_div)
	elif hop0 == 'd': 
		letters = crawler.retrieveFromSoup(_block='div',_class=dual_div)
	else: 
		print 'Not Valid Hop Type (aroma,bittering,dual)'

	return letters

def getEssentials(letters,knownProfiles=None): 
	'''
	'id', 'name','rating','url','aromas'
	STEP 3 (for each item from STEP 2)
	'''

	indivs = {}
	if knownProfiles == None: 
		knownProfiles = []

	for i,line in enumerate(letters): 
		indivs[i] = {}
		# hop id number 
		indivs[i]['id'] = line['data-id']

		# hop name 
		indivs[i]['name'] = line.find('img')['alt']

		# get hop rating (can be None, otherwise 0.0 - 5.0)
		try: 
			ratingValue = line.find('meta', itemprop='ratingValue')['content']
		except TypeError: 
			ratingValue = None
		indivs[i]['rating'] = ratingValue

		# get link 
		indivs[i]['url'] = line.find("a")['href']

		# get aroma profile
		hopAromas = []
		for aroma in line.findAll("a",itemprop="category"): 
			hopAromas.append(aroma.text.replace(',',''))
		indivs[i]['aromas'] = hopAromas
		
	return indivs 

def buildHopGroup(indivs, use, hopGroup=None): 
	from hop import Hop

	if hopGroup == None: 
		hopGroup = []

	for indiv in indivs.values(): 
		idnum,name,rating,url,aromas = indiv['id'],indiv['name'],indiv['rating'],indiv['url'],indiv['aromas']
		new_hop = Hop(idnum,name,use,rating,url,aromas)
		hopGroup.append(new_hop)

	return hopGroup

def buildFullHopGroup(aEss,bEss,dEss):
	''' STEP 4 ''' 
	hopGroup = buildHopGroup(aEss,'aroma')
	hopGroup = buildHopGroup(bEss,'bittering',hopGroup)
	hopGroup = buildHopGroup(dEss,'dual-purpose',hopGroup)
	return hopGroup

def printAttributes(indivs,attributes=None):
	if attributes == None: 
		attributes = ['id','name','rating','url','aromas']

	for indiv in indivs.values(): 
		printing = []
		for att in attributes: 
			if indiv[att] == None: 
				printing.append(att+': --')
			else:
				if type(indiv[att]) is list: 
					printing.append(att+': ['+', '.join(indiv[att])+' ]')
				else: 
					printing.append(att+': '+indiv[att])
		print '       \t'.join(printing)


def doToHopGrouping(): 

	#initialize the crawler
	crawler = initialize("https://ychhops.com/varieties")
	print 'Step 1/4 complete. (init souping) '

	#get the soup for the individual use types
	aromas, bitters, duals = getAllTypes(crawler)
	print 'Step 2/4 complete. (pick out letters)'

	#get the essential information from each hop use type
	aromaEss, bitterEss, dualEss = getEssentials(aromas), getEssentials(bitters), getEssentials(duals)
	print 'Step 3/4 complete. (define essentials)'

	#define the Hop objects 
	hopGroup = buildFullHopGroup(aromaEss, bitterEss, dualEss)
	print 'Step 4/4 complete. (hopGroup assembled)'

	return hopGroup

def addNewHopGroupInfo(hopGroup): 
	for curr_hop in hopGroup: 
		crawler = initialize(curr_hop.url)


		'''ADD OIL INFORMATION'''
		oilnames,oilvalues,uppers,lowers,middles,units = [],[],[],[],[],[]
		oilname_letters = crawler.retrieveFromSoup('div','hop-composition__item')		#get list elements with oil information
		oilvalue_letters = crawler.retrieveFromSoup('div','hop-composition__value')		#get list elements with oil information

		for oilname in oilname_letters:
			oilnames.append(oilname.text)

		print 'oilvalue letters: ', len(oilvalue_letters)
		for ov in oilvalue_letters: 
			#print 'OV', ov 
			if ov.text != None:
				#print 'ov; ', ov.text
				text = ov.text
				lower,upper,middle,unit = textutils.getMinMaxUnit(text)
			oilvalues.append(ov.text)
			lowers.append(lower)
			uppers.append(upper)
			middles.append(middle)
			units.append(unit)

		curr_hop.addOils(oilnames,oilvalues,uppers,lowers,middles,units)
		'''END ADD OIL INFORMATION'''

		'''ADD COUNTRY, GENERAL DESCRIPTION, AROMA DESCRIPTION'''



def completeHopGroup(): 
	hg = doToHopGrouping()
	addNewHopGroupInfo(hg)
	return hg

def makeOilsMatrix(hopGroup):
	num_hops = len(hopGroup)
	num_features = 11
	oils = np.zeros((num_hops,num_features))
	feature_names = [u'Alpha Acid', u'Beta Acid', u'Co-humulone', u'Total Oil', u'B-Pinene', u'Myrcene', u'Linalool', u'Caryophyllene', u'Farnesene', u'Humulene', u'Geraniol']
	hop_names = []
	for i,h in enumerate(hopGroup): 
		hop_names.append(h.name)
		for k,v in h.advanced_oil_description.iteritems():
			oils[i,feature_names.index(k)] = v['middle']

	return oils,hop_names,feature_names

def getKnownAromas(hopGroup): 
	known_aromas = []
	for i,h in enumerate(hopGroup): 
		for aroma in h.aromas: 
			if aroma not in known_aromas: 
				known_aromas.append(aroma)
	return known_aromas

def getAromaArray(hopGroup,known_aromas):
	aromaArray = np.zeros((len(hopGroup),len(known_aromas)))		# 0 means no aroma present, +1 means aroma present
	for i,h in enumerate(hopGroup):
		for a in h.aromas: 
			aromaArray[i,known_aromas.index(a)] = 1
	return aromaArray

def getOilsAndAromas(hopGroup):
	'''run completeHopGroup() first to get hopGroup'''
	oilsArray,hop_names,feature_names = makeOilsMatrix(hopGroup)
	known_aromas = getKnownAromas(hopGroup)
	aromaArray = getAromaArray(hopGroup,known_aromas)
	return [oilsArray,aromaArray],[hop_names,feature_names,known_aromas]

'''
Plan 
-----
0. Create a .csv file with all of the bounds and all of the hop names and put on git
0a. note which fields are missing data and make a plan to account for them
1. using technique with bounds on the styles, create a whole bunch of data points with the flavor descriptors 
2. split data into training, test, validation data
3. Learn about random forests - try to implement 
4. Run SGD 



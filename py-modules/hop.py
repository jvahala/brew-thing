
class Hop(object): 
	def __init__(self,idnum,name,use,rating,url,aromas): 
		self.id = idnum
		self.name = name
		self.use = use
		self.rating = rating
		self.url = url 
		self.aromas = aromas

	def addOils(self,oilnames,oilvalues,uppers,lowers,middles,units):
		self.oilnames = oilnames
		self.oilvalues = oilvalues
		self.uppers = uppers
		self.lowers = lowers 
		self.middles = middles
		self.units = units

		self.basic_oil_description = {}
		self.advanced_oil_description = {}

		for i,oilname in enumerate(oilnames): 
			self.basic_oil_description[oilname]=oilvalues[i]
			self.advanced_oil_description[oilname]={'lower':lowers[i],'middle':middles[i],'upper':uppers[i],'unit':units[i]}

	def printAll(self): 
		print '\n---------'
		print 'id: ',self.id
		print 'name: ', self.name
		print 'use: ', self.use
		print 'rating: ', self.rating
		print 'url: ', self.url
		print 'aromas: ', self.aromas 
		print '---------\n'

class Flavor(object): 
	def __init__(self,name):
		self.name = name 

	#def addHop(self,hopidnum): 
		
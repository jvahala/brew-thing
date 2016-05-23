from utils import residualco2

class style(object):
	'''

	'''
	def __init__(self, name):
		self.name = name
		self.malts = {}				#malt options {malt1: default percent, malt2: default percent}
		self.yeasts = []			#yeast options	[yeast1, yeast2, yeast3 ...] option1 is default for style
		self.hops = []				#hop options [hop1, hop2, hop3, ...]
		self.adjuncts = []			#other optional additions (e.g. orange peel, coriander, etc)
		self.ibu_range = [0,150] 	#[min_ibu, max_ibu]
		self.abv_range = [3, 10]	#[min_abv, max_abv]
		self.srm_range = [0, 20]	#[min_srm, max_srm]
		self.co2_range = [0,  5]	#[min_co2, max_co2]

class ingredient(object): 
	'''
	https://byo.com/resources/
	use this class for stuff like coriander, jasmine, other spices and stuff that doesnt have fermentable sugars and what not
	'''
	def __init__(self, name, styles, flavors):
		self.name = name
		self.styles = []			#list of styles typically with this malt
		self.flavors = {}			#{flavor1: strength in [0,1], flavor2: strength in [0,1] ...}

class malt(ingredient):
	'''
	https://byo.com/resources/grains
	includes additional sugars like candi syrups or malt extract 
	'''
	def __init__(self,name,styles,flavors,color,gravity):
		super().__init__(name,styles,flavors)
		self.color = color				#color in degrees Lovibond
		self.gravity = gravity			#gravity from 1 lb in 1 gallon of water 
		

class yeast(ingredient):
	'''
	https://byo.com/resources/yeast
	'''
	def __init__(self,name,styles,flavors,temp_range,attenuation,flocculation):
		super().__init__(name,styles,flavors)
		self.temp_range = temp_range		#[min_temp, max_temp]
		self.attenuation = attentuation		#attenuation in [0,1]
		self.flocculation = flocculation 	#flocculation 'low','med','high'


class hop(ingredient):
	'''
	https://byo.com/resources/hops
	'''
	def __init__(self,name,styles,flavors,alphaacid):
		super().__init__(name,styles,flavors)
		self.aa = alphaacid 				#alpha acid percent in [0,1]


class primer(object):
	'''
	https://byo.com/resources/carbonation
	may just want a function that assumes you are using sucrose (table sugar) dissolved in water instead of allowing for multiple priming sources...because thats kind of pointless anyways
	'''
	def __init__(self,name,prime_table):
		self.name = name
		self.prime_table = prime_table		#n by 2 array of n [grams_primer, vol co2 per 5 gallons] entries

	def volsToGrams(self,batch_size,ferm_temp,vols):
		'''
		Computes conversion from vols co2 to grams of primer at a fermentation temperature, batchsize, and such 
		'''
		residual = residualco2(ferm_temp)
		priming_needed = vols - residual 
		##add interpolation for prime_table: self.grams_needed = interpolation(prime_table, priming_needed) 

		return self.grams_needed
		

			

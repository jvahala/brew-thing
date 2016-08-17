# module for taking input data [OG,FG,ABV,SRM,IBU] and outputing the styles this fits 
import numpy as np 
import utils


np.set_printoptions(threshold=np.nan,precision=3,suppress=True)

class Vitals(object): 
	def __init__(self,stylename='undefined',vitals=None):
		if vitals == None: 
			vitals = {'OG':[1.030,1.060],'FG':[1.000,1.010],'ABV':[4.0,6.0],'SRM':[2.0,4.0],'IBU':[25, 40]}
		self.vitals = vitals
		self.stylename = stylename 
		self.vitals = vitals 	#all elements in vitals are elt:[min,max] representing the range for a style
		self.order = ['OG','FG','ABV','SRM','IBU']

	def randomizeVitals(self): 
		def newBounds(lowmin,lowmax,lowhighdiff,decimals): 
			newlow = round(randomBetween(lowmin,lowmax),decimals)
			highmin = 1.005*newlow 
			newhigh = round(randomBetween(highmin,highmin+lowhighdiff),decimals)
			return newlow,newhigh

		for v in self.order: 
			if v == 'OG': 
				newlow,newhigh = newBounds(1.020,1.060,0.010,3)
				self.vitals[v][0] = newlow
				self.vitals[v][1] = newhigh 
			if v == 'FG': 
				newlow,newhigh = newBounds(1.000,1.010,0.0010,3)
				self.vitals[v][0] = newlow
				self.vitals[v][1] = newhigh 
			if v == 'ABV': 
				newlow,newhigh = newBounds(3.0,6.0,3,1)
				self.vitals[v][0] = newlow
				self.vitals[v][1] = newhigh 
			if v == 'SRM': 
				newlow,newhigh = newBounds(1.0,9.0,4.0,1)
				self.vitals[v][0] = newlow
				self.vitals[v][1] = newhigh 
			if v == 'IBU': 
				newlow,newhigh = newBounds(5,40,30,0)
				self.vitals[v][0] = newlow
				self.vitals[v][1] = newhigh 

	def checkValidity(self,newvitals): 
		for i,v in enumerate(newvitals): 
			if v > self.vitals[self.order[i]][0] and v < self.vitals[self.order[i]][1]: 
				continue 
			else: 
				return 0
		return 1

	def makeTrainingData(self,n=10,labels=[]): 
		train = np.zeros((n,len(self.vitals)))		#n by len(vitals) array for training
		for i,row in enumerate(train): 
			for j,k in enumerate(self.order): 
				train[i,j] = randomBetween(self.vitals[k][0],self.vitals[k][1])
		return train,labels 


	def makeTestData(self,t=10): 
		test = np.zeros((k,len(self.vitals)))		#t by len(vitals) array for testing

def randomBetween(low,high): 
	return low + np.random.rand()*(high-low)

def main(): 
	np.random.seed(1)	#good practice 
	numStyles = 5
	examplesPerStyle = 50
	testsPerStyle = 10
	n = numStyles*examplesPerStyle
	t = numStyles*testsPerStyle

	#set up training data
	train_data = np.zeros((n,5))		#5 different vital traits
	test_data = np.zeros((t,5))			
	styles = {}
	for i in np.arange(numStyles): 
		styles[i] = Vitals(stylename=('style'+str(i)))
		styles[i].randomizeVitals()
		ind1 = examplesPerStyle*i
		ind2 = ind1+examplesPerStyle
		ind3 = testsPerStyle*i
		ind4 = ind3+testsPerStyle
		train_data[ind1:ind2,:],labels = styles[i].makeTrainingData(n=examplesPerStyle)
		test_data[ind3:ind4,:], labels = styles[i].makeTrainingData(n=testsPerStyle)

	#set up labels for training data
	train_labels = np.zeros((n,numStyles))
	test_labels = np.zeros((t,numStyles))
	for i,row in enumerate(train_data): 
		for k,sty in enumerate(styles): 
			train_labels[i,k] = styles[sty].checkValidity(row)
	for i,row in enumerate(test_data):
		for k,sty in enumerate(styles):
			test_labels[i,k] = styles[sty].checkValidity(row)

	#get nearest neighbors within some distance threshold of the max for each test case
	mostlikely = np.zeros((1,numStyles))
	for tester in test_data: 
		sorted_inds,dists = utils.sortedDists(tester,train_data)

		max_dist = dists[sorted_inds[-1]]
		dists = [dists[x] for x in sorted_inds]

		dist_consider_threshold = 0.25
		dist_arg = np.argmax(dists>dist_consider_threshold*dists[-1])

		classprops = np.zeros((1,numStyles))
		for ind in sorted_inds[0:dist_arg]: 
			classprops = classprops + train_labels[ind,:]

		classprops = classprops/dist_arg
		sortprops = np.argsort(classprops)[0]
		print classprops,sortprops 
		besttwo = classprops[0,sortprops[-1]]+classprops[0,sortprops[-2]]
		best1 = classprops[0,sortprops[-1]]/besttwo
		best2 = classprops[0,sortprops[-2]]/besttwo
		if best1 > 0.66: 
			classprops = np.zeros_like(classprops)
			classprops[0,sortprops[-1]] = 1
		else: 
			classprops = np.zeros_like(classprops)
			classprops[0,sortprops[-1]],classprops[0,sortprops[-2]] = best1, best2
		
		mostlikely = np.vstack((mostlikely,classprops))




	return styles,train_data,train_labels,sorted_inds,dists,mostlikely

#0. define S styles by vital statistics 

#1. make a training data set for several styles 
#		X = n by 5 training set

#2. go through each row and assign whether it is in a style or not as output labels 
#		Y = n by S label set 

#3. send training and label set through neural network to get weights on labels 

#4. profit






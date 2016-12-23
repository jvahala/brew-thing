import numpy as np

def residualco2(ferm_temp):
	'''
	Purpose: 
		gets residual co2 from fermentation at a given temperature using https://byo.com/resources/carbonation table B

	Inputs: 
		ferm_temp - temperature at which fermentation was performed

	Outputs: 
		residual co2 at the input ferm_temp
	'''
	
	temps = range(47,84,3)			#in degrees F from source table B
	resids = [1.21,1.15,1.09,1.04,0.988,0.940,0.894,0.850,0.807,0.767,0.728,0.691,0.655]	#residual co2 for the different temps
	if ferm_temp in temps: 
		return resids[temps.index(ferm_temp)]
	else: 
		lower = [x for x in temps if (ferm_temp-x)<3 and (x-ferm_temp)<0]
		upper = [x for x in temps if (x-ferm_temp)<3 and (ferm_temp-x)<0]
		lower_ind = temps.index(lower[0])
		upper_ind = temps.index(upper[0])
		slope = (resids[upper_ind]-resids[lower_ind])/(temps[upper_ind]-temps[lower_ind])
		return resids[lower_ind] + slope*(ferm_temp-temps[lower_ind])

def euclideanDist(point1,point2): 
	'''
	Purpose: 
	Calculates euclidean distance between two points

	Inputs: 
	point1,point2 - same dimensioned points in some space 

	Outputs: 
	output - euclidean distance between the two points, ||point1-point2||_2

	'''
	return np.linalg.norm(point1-point2)

def majorityVote(values): 
	'''
	Purpose: 
	Outputs the most often seen values from a 1d list/array of values along with a list of the sorted indices and sorted values by majority vote 

	Inputs: 
	values - 1d list/array of values that include redundant values 

	Outputs: Two outputs - output1,output2
	output1 - the most often counted value that was found in values 
	output2 - list with two components = [sorted unique values from least often to most often, counts corresponding to the unique values]

	'''
	'''test code (place on own as main)
	x1 = [2]*5+[1]*10+[0]*3			# expected list return- [0,2,1], [3,5,10]
	x2 = [1]*5+[2]*10+[0]*3			# [0,1,2], [3,5,10]
	x3 = [0]*5+[1]*10+[2]*3			# [2,0,1], [3,5,10]
	x4 = [0]*5+[2]*10+[1]*3			# [1,0,2], [3,5,10]
	x5 = [2]*5+[0]*10+[1]*3			# [1,2,0], [3,5,10]
	x6 = [2]*10+[1]*5				# [1,2], [5,10]

	def dothings(x): 
		print x 
		best_val, obj = majorityVote(x)
		print 'most often: ', best_val 
		print 'sorted indicies: ', obj[0]
		print 'sorted count values for indicies: ', obj[1]

	dothings(x1)
	dothings(x2)
	dothings(x3)
	dothings(x4)
	dothings(x5)
	dothings(x6)
	'''
	#print 'np.unique(values): ', np.unique(values), values
	if isinstance(values,list): 
		uValues = np.unique(values).tolist()
		uCounts = [np.sum(np.array(values) == uv) for uv in uValues]
		sorted_inds = np.argsort(uCounts)
		best_val = uValues[sorted_inds[-1]]
		sorted_vals = [int(uValues[x]) for x in sorted_inds]
		sorted_cnts = np.sort(uCounts)
	else: 
		best_val = values 
		sorted_vals = values
		sorted_cnts = len(values)
	return best_val, [sorted_vals, sorted_cnts]

def sortedDists(new_point, known_points): 
	'''
	Purpose: 
	Uses euclidean distances to get ordered closest points to new point. Need to give the new point and the past labeled points and labels along with the number of past points to choose the new point label from. This version returns the indices in history_points along with the maximum distance. It does not return the labels. 

	Inputs: 
	new_point - 1 by p array representing the new p-featured point in space 
	history_points - n by p array representing the known labeled points in space 
	k - nearest neighbors to consider for choosing new point label. The majority vote label from the k closest points to the new point will be output as the new label.

	Outputs: Two outputs in a single list object - [vote,counts_info]
	sorted_inds - indices sorted by closest distance to the new point 
	distances - all distances 
	'''
	distances = []
	for old_point in known_points: 
		distances.append(euclideanDist(new_point,old_point))
	sorted_inds = np.argsort(distances)
	return sorted_inds,distances


def runningAvg(vector,N): 
	'''
	Purpose: 
	Performs a runningAvg calculation on a 1d array 'vector' and averages over N spaces 

	Inputs: 
	vector - ndarray 1-dimensional array 
	N - number of elements to average over 

	Outputs: 
	vector with each element being the runningAvg over N elements - same size as original vector

	'''
	return np.convolve(vector, np.ones(N,)/(N*1.0))[(N-1):]

def randomBetween(low,high): 
	return low + np.random.rand()*(high-low)


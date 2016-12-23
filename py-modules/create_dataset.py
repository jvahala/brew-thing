'''
ensemble classifiers script using tools from scikit-learn
'''

import pandas as pd 
import numpy as np 
from stylize import randomBetween 
import ast

def loadData(filename='HopData.csv'): 
	return pd.read_csv(filename,skiprows=[1])

def chooseDataSubset(dataframe,col_subset=range(4,41)): 
	subset = dataframe[dataframe.columns[col_subset]][0:]
	print subset 
	return subset 

def fillNaN(dataframe, value): 
	'''returns a new dataframe with all NaNs filled with 'value' '''
	return dataframe.fillna(value)

def createDataframe(_array,_columns): 
	return pd.DataFrame(data=_array,columns=_columns)

def generateData(dataframe, N=1000, seed=1):
	np.random.seed(1)

	# gather relevant data
	#num_col = len(dataframe.columns)		#41 for initial HopData.csv
	#subset = chooseDataSubset(dataframe,col_subset=range(4,num_col))
	
	# define X from relevant data
	#X = np.zeros((N,11))
	#Y = np.zeros((N,1))		#will add to this as more aromas are discovered
	#all_aromas = []

	# select random hop row, fill out the 11 rows 
	#[alpha, beta, cohum, totoil, Gera, Cary, Bpine, Myrce, Humu, Lina, Farne]

	# while dataset not filled out
	hop_select_order = filloutN(len(dataframe),N)

	print 'hop_select_order: ', hop_select_order
	curr_row = 0

	# column names for the new dataframe (base info / key traits / oil percentages / calculated features)
	column_names = [
	'name', 'url', 'use', 'rating', 'aromas', 
	'alpha', 'beta', 'cohumulene', 'totalOil', 
	'geraniol', 'caryophyllene', 'bPinene', 'myrcene', 'humulene', 'linalool', 'farnesene'
	]

	new_data = np.empty((N,len(column_names)), dtype=object)
	curr_ind_position = 0
	for hop_num,count in hop_select_order.iteritems(): 
		for c in range(count): 
			# add basic stuff (name, url, use, rating, aromas)
			new_data[curr_ind_position,0] = dataframe['name'][hop_num]
			new_data[curr_ind_position,1] = dataframe['url'][hop_num]
			new_data[curr_ind_position,2] = dataframe['use'][hop_num]
			new_data[curr_ind_position,3] = dataframe['rating'][hop_num]
			new_data[curr_ind_position,4] = dataframe['aromas'][hop_num]

			# add randomized oil information
			new_data[curr_ind_position,5] = randomBetween(dataframe['Alpha Acid-low'][hop_num], dataframe['Alpha Acid-high'][hop_num])
			new_data[curr_ind_position,6] = randomBetween(dataframe['Beta Acid-low'][hop_num], dataframe['Beta Acid-high'][hop_num])
			new_data[curr_ind_position,7] = randomBetween(dataframe['Co-humulone-low'][hop_num], dataframe['Co-humulone-high'][hop_num])
			new_data[curr_ind_position,8] = randomBetween(dataframe['Total Oil-low'][hop_num], dataframe['Total Oil-high'][hop_num])

			new_data[curr_ind_position,9] = randomBetween(dataframe['Geraniol-low'][hop_num], dataframe['Geraniol-high'][hop_num])
			new_data[curr_ind_position,10] = randomBetween(dataframe['Caryophyllene-low'][hop_num], dataframe['Caryophyllene-high'][hop_num])
			new_data[curr_ind_position,11] = randomBetween(dataframe['B-Pinene-low'][hop_num], dataframe['B-Pinene-high'][hop_num])
			new_data[curr_ind_position,12] = randomBetween(dataframe['Myrcene-low'][hop_num], dataframe['Myrcene-high'][hop_num])
			new_data[curr_ind_position,13] = randomBetween(dataframe['Humulene-low'][hop_num], dataframe['Humulene-high'][hop_num])
			new_data[curr_ind_position,14] = randomBetween(dataframe['Linalool-low'][hop_num], dataframe['Linalool-high'][hop_num])
			new_data[curr_ind_position,15] = randomBetween(dataframe['Farnesene-low'][hop_num], dataframe['Farnesene-high'][hop_num])

			curr_ind_position += 1

	# create the new DataFrame object
	dataset = createDataframe(new_data,column_names)

	# remove Nan values from the actual percentage oil data and replace with zero
	dataset.iloc[:,9:16].fillna(0,inplace=True)

	# fill in cohumulene column Nan values with median based on the use type
	dataset = fillCohumuleneNan(dataset) 

	# change the datatypes of numbered values to floats
	dataset.info()
	for col in range(5,16): 
		dataset.iloc[:,col] = dataset.iloc[:,col].astype(float)
	dataset.info()

	# add unknown column 
	dataset['unknown'] = 100 - np.sum(dataset.iloc[:,9:16],axis=1)

	# add aroma information 
	all_aromas = allAromas(dataset.aromas) 		#get which aromas exist in the dataset
	A = arrayOfAromas(dataset.aromas,all_aromas)	# define an array with 1's in places where an aroma is present
	aromaset = createDataframe(A,all_aromas)

	# concatenate aromaset onto dataset
	full_dataset = dataset.join(aromaset)

	return full_dataset

def allAromas(aromas_col): 
	all_aromas = []
	for _set in aromas_col: 
		list_set = ast.literal_eval(_set)
		for aroma in list_set: 
			if aroma not in all_aromas: 
				all_aromas += [aroma]
	return all_aromas

def arrayOfAromas(aromas_col,all_aromas):
	A = np.zeros((len(aromas_col),len(all_aromas))) 
	for i,_set in enumerate(aromas_col): 
		list_set = ast.literal_eval(_set)
		for aroma in list_set: 
			A[i,all_aromas.index(aroma)] = 1
	return A 



def filloutN(num_types, N):
	order_list = np.random.permutation(num_types)
	base_examples_per_selection = N/len(order_list)
	base_sum = base_examples_per_selection*len(order_list)
	num_remaining = N - base_sum
	order_dict = {}
	for example in order_list: 
		order_dict[example] = base_examples_per_selection
		if num_remaining > 0: 
			order_dict[example] += 1
			num_remaining -= 1
	return order_dict

def fillCohumuleneNan(dataset):
	#fill aroma Nans 
	aroma_median = dataset.cohumulene[dataset.use=='aroma'].median()
	dataset.cohumulene[dataset.use=='aroma'] = dataset.cohumulene.loc[dataset.use=='aroma'].fillna(aroma_median)
	#fill bittering Nans
	bittering_median = dataset.cohumulene[dataset.use=='bittering'].median()
	dataset.cohumulene[dataset.use=='bittering'] = dataset.cohumulene.loc[dataset.use=='bittering'].fillna(bittering_median)
	#fill dual-purpose Nans
	dual_median = dataset.cohumulene[dataset.use=='dual-purpose'].median()
	dataset.cohumulene[dataset.use=='dual-purpose'] = dataset.cohumulene.loc[dataset.use=='dual-purpose'].fillna(dual_median)
	return dataset


def main(): 
	dataframe = loadData('HopData.csv')
	dataset = generateData(dataframe,10000)

	return dataset 



if __name__ == '__main__': 
	main()
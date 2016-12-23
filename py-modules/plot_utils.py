import matplotlib.pyplot as plt 
import seaborn as sns 
import numpy as np
import pandas as pd

'''
general strategies: 
barChart - 
	create an nxk array of data where the k columns are individual bars you want and the n data are the elements to be stacked on top of each other
	create a labels list with the labels for each of the n elements 
	turn this into a pd.DataFrame object and call barChart with the valid columns that you want to show and the x and y labels
'''

def barChart(dataframe,valid_columns=None):
	flatui = [ "#e74c3c","#3498db", sns.xkcd_rgb["soft pink"], "#9b59b6", "#34495e", sns.xkcd_rgb["light sky blue"],"#95a5a6","#2ecc71",]
	sns.set_palette(flatui)
	sns.set_style('whitegrid')
	if valid_columns == None: 
		# all columns valid 
		fig = dataframe.plot(kind='bar',stacked=True)
		sns.despine(left=True)

	else: 
		# only show the valid columns on the chart 
		pass

def plotScatter(dataframe,column_name,legend='all',title=None,show_all_index_ticks=True):
	if title == None: 
		title = column_name
	if show_all_index_ticks: 
		ax = dataframe[column_name].plot(style='s')
		ticks = list(dataframe.index)
		plt.xticks(range(len(ticks)),ticks,rotation=90)
		plt.tight_layout()
		plt.title(title)
		plt.xlabel('Percent of Total Oil (%)')


def getAvgs(hop_df,unique_types=127,use='all'):
	#changing use to 'bittering' or 'aroma' or 'dual-purpose' makes it so the resulting A_df is dependent only on these types of hops
	#this function gets the individual hop average values for each of the numeric columns 
	known_names = []
	A_ind = -1
	A = np.zeros((127,24))
	labels = hop_df.columns[5:]
	for i,elt in hop_df.iterrows(): 
		if use != 'all': 
			if elt.use != use:
				continue 

		if elt['name'] not in known_names: 
			A_ind += 1
			known_names.append(elt['name'])
			indices = hop_df.name == elt['name']
			data_selection = hop_df.iloc[:,5:17][indices]
			avgs = np.mean(data_selection)
			#stds = np.std(data_selection)
			aromas = hop_df.iloc[i,17:]
			#print aromas 
			A[A_ind,0:12] = avgs
			A[A_ind,12:] = aromas
	A_df = pd.DataFrame(data=A,columns=labels)
	return A_df 

def getAromaBasedAvgs(A_df): 
	#this function accepts the set of hop average values and turns it into a set of average values based on which hops have which flavor profiles.
	aromas = A_df.columns[12:]
	AromaAvg = np.zeros((len(aromas),12))
	for i,a in enumerate(aromas): 
		selection = A_df[a]==1
		AromaAvg[i,:] = np.mean(A_df.iloc[:,0:12][selection],axis=0)
		std = np.std(A_df.iloc[:,0:12][selection],axis=0)
		print a, std
	AromaAvg_df = pd.DataFrame(AromaAvg,index=aromas,columns=A_df.columns[0:12])
	return AromaAvg_df

def getUseSubsets(dataframe):
	#utility function to get all the wanted subsets without a lot of typing
	A_aroma,A_bitter,A_dual,A_all = getAvgs(dataframe,use='aroma'), getAvgs(dataframe,use='bittering'), getAvgs(dataframe,use='dual-purpose'), getAvgs(dataframe,use='all')
	Aa_aroma,Aa_bitter,Aa_dual,Aa_all = getAromaBasedAvgs(A_aroma), getAromaBasedAvgs(A_bitter), getAromaBasedAvgs(A_dual), getAromaBasedAvgs(A_all)
	subset_examples, subset_aromas = [A_aroma,A_bitter,A_dual,A_all], [Aa_aroma,Aa_bitter,Aa_dual,Aa_all]
	return subset_examples,subset_aromas
	
def plotAromaOils(hop_10kdf,total_unique=127,valid_columns=None,scale=True,use='all'):
	#does full analysis of a dataset of many hop examples and plots the bar plot of flavors with bars composed of individual oils
	A_df = getAvgs(hop_10kdf,total_unique,use=use)
	AromaAvg_df = getAromaBasedAvgs(A_df)
	if scale: 
		Aplot = AromaAvg_df.iloc[:,4:].multiply(0.01*AromaAvg_df.totalOil,axis=0)
		barChart(Aplot,valid_columns)
		plt.ylabel('Mean Oil Composition (mL/100g)')
		if use == 'bittering': 
			plt.ylim([0,3.5])
		else:
			plt.ylim([0,2.5])
		plt.legend(ncol=4)
	else: 
		Aplot = AromaAvg_df.iloc[:,4:] 
		barChart(Aplot,valid_columns)
		plt.ylabel('Mean Percent of Total Oil (%)')

		plt.ylim([0,119])
		plt.legend(ncol=4)

	plt.tight_layout()


def main(): 
	pass



if __name__ == '__main__': 
	main()
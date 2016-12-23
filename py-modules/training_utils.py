import copy

def segmentUseTypes(dataset): 
	#dataset = full dataset including all name information from create_dataset.generateData()
	Xaroma = dataset[dataset.use=='aroma'].iloc[:,5:]	#alpha to the rest
	Xbitter = dataset[dataset.use=='bittering'].iloc[:,5:] 
	Xdual = dataset[dataset.use=='dual-purpose'].iloc[:,5:]
	Xall = dataset.iloc[:,5:]

	#remove items that have an unknown oil amount greater than 50% 
	Xaroma = Xaroma[Xaroma['unknown']<50]
	Xbitter = Xbitter[Xbitter['unknown']<50]
	Xdual = Xdual[Xdual['unknown']<50]
	Xall = Xall[Xall['unknown']<50]

	#separate X and Y
	Yaroma = Xaroma.iloc[:,12:]
	Ybitter = Xbitter.iloc[:,12:]
	Ydual = Xdual.iloc[:,12:]
	Yall = Xall.iloc[:,12:]

	Xaroma = Xaroma.iloc[:,0:12]
	Xbitter = Xbitter.iloc[:,0:12]
	Xdual = Xdual.iloc[:,0:12]
	Xall = Xall.iloc[:,0:12]


	X = {'aroma':Xaroma, 'bitter':Xbitter, 'dual':Xdual, 'all':Xall }
	Y = {'aroma':Yaroma, 'bitter':Ybitter, 'dual':Ydual, 'all':Yall }
	return X,Y


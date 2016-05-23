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
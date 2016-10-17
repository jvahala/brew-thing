import string

def getMinMaxUnit(text): 

	test = text.rpartition('-')[0]

	if test == '': 
		if text.rpartition('%')[0] == '': 
			pct = float(text)
			lower = pct
			higher = pct 
			mean = pct 
		else: 
			base = text.rpartition('%')[0]
			if '<' in base: 
				lower = 0.0
				higher = float(base[base.index('<')+1:])
				mean = higher/2.0 
			if '>' in base: 
				lower = float(base[base.index('>')+1:])
				higher = lower + 2.0
				mean = lower+1.0
	else: 
		if text.rpartition('%')[0] == '': 
			lower = float(test)
			higher = float(text.partition('-')[-1].rpartition('m')[0])
			mean = (lower+higher)/float(2)
		else: 
			lower = float(text.rpartition('-')[0])
			higher = float(text.partition('-')[-1].rpartition('%')[0])
			mean = (lower+higher)/float(2)

	if text.rpartition('%')[0]  == '': 
		unit = 'm'+text.rpartition('m')[-1]
	else:
		unit = '%'+text.rpartition('%')[-1]

	return lower, higher, mean, unit


'''test = ['0.4 - 0.6% of total oil',
'3.5 - 6.5%',
'4 - 6%',
'30 - 34%',
'0.5 - 1.7 mL/100g',
'0.6 - 0.9% of total oil',
'45 - 55% of total oil',
'0.4 - 0.6% of total oil',
'9 - 12% of total oil',
'< 1.0% of total oil',
'15 - 22% of total oil',
'0.4 - 0.7% of total oil']'''

#getMinMaxUnit(test[11])


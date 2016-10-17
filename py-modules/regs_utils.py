import numpy as np

def svd(X):
	U,S,V = np.linalg.svd(X,full_matrices=False)
	return U,S,V

def convertY(y,convertfrom=0):
	if convertfrom == 0: 
		#convert from 0/1 to -1/1
		z = [-1 if x == 0 else 1 for x in y]
	else: 
		z = [0 if x == -1 else 1 for x in y]
	return np.array(z).reshape(len(z),1)

def regression(X,y,const=True,loss='ls',reg=None,reg_lambda=1,ytype='01'):
	'''
	Purpose: 
	Solves for weights w in to solve min_w ||Xw-y|| + \lambda||w|| under a loss and regularizer using inverse calculation methods. See alternate function for gradient descent solver.

	Inputs: 
	X = ndarray of n elements by k features
	w = weights (k by 1)
	y = labels (k by 1)
	loss = 
		'ls' - least squares f(x) = ||x||^2 
		'log' - logarithmic loss f(x) = 1/n sum 1/(exp something)
	reg = (adds + reg_lambda*reg(x)) term
		'none' - not regularizer
		'ridge' - add reg_lambda*||w||_2^2
		'lasso' - add reg_lambda*||w||_1
	reg_lambda = parameter associated with regularizer 
	'''

	# what = (X'X)^-1 X' y
	if ytype == '01': 
		y = convertY(y,0)
	if const: 
		X = np.hstack((X,np.ones((len(X),1))))
	if reg == None: 
		if loss == 'ls': 
			XtX = np.dot(X.T,X)
			XtXinv = np.linalg.inv(XtX)
			XtXinvXt = np.dot(XtXinv,X.T)
			w_hat = np.dot(XtXinvXt,y)
	return w_hat 

def generateData(N,form='bull',dim=2):
    '''
	Purpose: 
	Generates (N by dim) ndarray of a type described by 'form'
	Particularly useful for testing clustering methods 

	Inputs: 
	N - length of data set
	dim - number of dimensions in dataset (ie dim = 2) 
	form - data set type
		--'sep' compiles a dataset with two distinct groups 
		--'bull' compiles a dataset of a bullseye shape (one labeled group within a ring of the other group)
		--'chain' compiles a dataset of a linear chain with a label break in between them

	Outputs: 
	X - compiled data array of 'form' type
	y - labels associated with each of the N examples of X 

	'''

    X = np.zeros((N,dim),dtype = np.float16)
    y = np.zeros((N,1), dtype = np.int_)
    
    if form == 'sep': #seperate clusters of data
        base1 = np.ones((1,dim))
        base2 = np.zeros((1,dim))
        cnt = 0
        while cnt < np.floor(N/2): 
            X[cnt,:] = base1 + 0.5*(np.random.rand(1,dim)*2.0-1.)
            y[cnt] = 1
            cnt += 1
        while cnt < N:
            X[cnt,:] = base2 + 0.5*(np.random.rand(1,dim)*2.0-1.)
            y[cnt] = -1
            cnt += 1
        y.shape = (N,)
        return X,y

    elif form == 'bull': #inner cluster surrounded by ring of points
        cnt=0;
        X = np.zeros((N,dim),dtype = np.float16)
        y = np.zeros((N,1), dtype = np.int_)
        totalg1 = 0
        totalg2 = 0
        while cnt < N :
            x = 2*np.random.rand(1,dim)-1;
            if np.linalg.norm(x) < 0.15 and totalg1<=(N-np.floor(N/1.2)):
                X[cnt,:] = x;
                y[cnt] = +1
                cnt=cnt+1;
                totalg1 +=1
            elif (np.linalg.norm(x) > 0.5 and np.linalg.norm(x) < 0.55) and totalg2<(N-(N-np.floor(N/1.2))):
                X[cnt,:] = x;
                y[cnt] = -1
                cnt=cnt+1;
                totalg2 += 1
        y.shape = (N,)
        return X,y

    elif form == 'chain': #linear chain graph of N points
    	X = np.zeros((N,dim),dtype = np.float16)
    	for i in np.arange(N):
    		X[i,:] = i
    		if i < N/2.:
    			y[i] = +1
    		else: 
    			y[i] = -1
    	y.shape = (N,)
       	return X,y

def plot2Dsplit(X,y,w,ys='01',cols=[0,1]): 
	import matplotlib.pyplot as plt 
	if ys == '01':
		y1,y2 = 0,1
	elif ys == '11':
		y1,y2 = -1,1
	plt.plot(X[y==y1,cols[0]],X[y==y1,cols[1]],'sr',label = 'Type '+str(y1))
	plt.plot(X[y==y2,cols[0]],X[y==y2,cols[1]],'dk',label = 'Type '+str(y2))

	wx = np.linspace(np.amin(X[:,cols[0]]),np.amax(X[:,cols[0]]),100)
	wy = -w[cols[0]]/float(w[cols[1]])*wx - w[-1]

	plt.plot(wx,wy,'-')
	plt.show()

#X,y = generateData(20,'sep',dim=3)
#w = regression(X,y)
#w = [a,b]  ax1 + bx2 + c = 0, x2 = -a/b x1 -c

#plot2Dsplit(X,y,w,'11',cols=[0,2])
#plt.show()



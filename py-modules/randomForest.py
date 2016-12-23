import numpy as np 
import pandas as pd 
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

def randomForestCrossVal(X,Y,n_estimators=10,max_depth=None):
	clf = RandomForestClassifier(n_estimators=n_estimators,max_depth=max_depth)
	scores = cross_val_score(clf,X,Y)
	print scores.mean()
	return scores 
	

def randomForest(Xtrain,Xtest,Ytrain,Ytest,n_estimators=10,max_depth=None):
	clf = RandomForestClassifier(n_estimators=n_estimators,max_depth=max_depth)
	clf = clf.fit(Xtrain,Ytrain)
	clf.predict(Xtest)
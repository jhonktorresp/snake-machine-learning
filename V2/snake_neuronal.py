from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
import pandas as pd

from joblib import dump, load



def training_model(neighbors):
	#Import data

	names = ["x","y","up","left","down","rigth","left","keep","right","score"]
	dataframe = pd.read_csv("snake_data.csv", names=names)

	array = dataframe.values	
	X, y = array[:, :-1], array[:, -1]

	X_train,X_test,y_train,y_test = train_test_split(X,y,test_size = 1)
	#Classifier
	print("number")
	print(array.shape[0])
	if(array.shape[0]<80):
		neighbors = array.shape[0]-1
	#my_classifier = KNeighborsClassifier(n_neighbors=neighbors)
	#my_classifier = RandomForestClassifier(max_depth=20, n_estimators=100, max_features=9)
	my_classifier = RandomForestClassifier(max_depth=20, n_estimators=100, max_features=9)
	#my_classifier = LogisticRegression()
	#my_classifier = LinearRegression()
	
	my_classifier.fit(X_train,y_train)
	
	predictions = my_classifier.predict(X_test)
	
	#my_testing = [
	#	[0,0,1,0,0,0,1,0,0],
	#	[0,0,1,0,0,0,0,1,0],
	#	[0,20,0,1,0,0,0,1,0],
	#	[1,20,0,1,0,0,0,1,0],
	#	[20,0,1,0,0,0,0,1,0],
	#	[3,4,1,0,0,0,0,1,0],
	#	[29,17,0,0,0,1,0,1,0],
	#	[1, 16, 0, 1, 0, 0, 0, 0, 1],
	#	[1, 16, 0, 1, 0, 0, 0, 1, 0],
	#	[1, 16, 0, 1, 0, 0, 1, 0, 0],
	#	[29,13,0,0,0,1,0,1,0]
	#]
	#
	dump(my_classifier, 'snake_model.joblib') 

	#predictions_2 = my_classifier.predict(my_testing)
	#
	#print(predictions_2)
	#print([1,1,1,0,1,0,1,0,1,0,1])
	#print(accuracy_score(y_test,predictions))

	

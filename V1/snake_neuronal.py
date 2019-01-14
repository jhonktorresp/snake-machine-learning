from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

from joblib import dump, load

def main():
	#Import data

	names = ["x","y","up","left","down","rigth","left","keep","right","score"]
	dataframe = pd.read_csv("snake_data.csv", names=names)

	array = dataframe.values	
	X, y = array[:, :-1], array[:, -1]

	X_train,X_test,y_train,y_test = train_test_split(X,y,test_size = 1)
	#Classifier
	my_classifier = KNeighborsClassifier()

	
	my_classifier.fit(X_train,y_train)
	
	predictions = my_classifier.predict(X_test)
	

	
	dump(my_classifier, 'snake_model.joblib') 


	

	
	
main()

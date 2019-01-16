import sys
import pandas as pd

from snake_visual import generate_learning_data,test_snake_machine
from snake_neuronal import training_model

def generate_more_data(number_per_session,see_training_try,x_init,y_init):
	
	dfmain = pd.read_csv("snake_data.csv",index_col=0)

	new_data = generate_learning_data(False,number_per_session,see_training_try,x_init,y_init)
	
	df2=pd.DataFrame(new_data,columns=["0","1","2","3","4","5","6","7","8","9"])

	dfmain=dfmain.append(df2, ignore_index=True,sort=False)
	print("Number of data:",dfmain.shape)

	dfmain.to_csv("snake_data.csv")		
	

def training_session(number_session,number_per_session):
	see_training_try = False
	x_init = 27
	y_init = 12
	neighbors = number_per_session
	for x in range(number_session):
		print("SESSION: ",x)
		#generate_more_data(number_per_session,see_training_try,x_init,y_init)
		training_model(neighbors)
		test_snake_machine(True,10,x_init,y_init)

def main():
	#80 neigthbors
	training_session(300,160)
	
main()
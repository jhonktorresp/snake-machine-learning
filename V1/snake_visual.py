import pygame,time,math
from snake_logic import snake
from pygame.locals import *
import numpy
import pandas
from joblib import dump, load
#import csv

	
limit_barrier = 30
width = 500
height = 500
pixel_w = width/limit_barrier
pixel_h = height/limit_barrier

white=(255,255,255)
black=(0,0,0)
green=(0,255,0)
	
def erase_board(display):
	pygame.draw.rect(display,black,(pixel_w,pixel_h,pixel_w*(limit_barrier-2),pixel_h*(limit_barrier-2)))	
	
def draw_path_board(display,explored):
	for x in range(0,limit_barrier):
		for y in range(0,limit_barrier):
			if(explored[x][y]):
				pygame.draw.rect(display,green,(x*pixel_w,y*pixel_h,pixel_w,pixel_h))				
	
def draw_pixel(display,x,y,explored):
	erase_board(display)
	draw_path_board(display,explored)
	pygame.draw.rect(display,white,(x*pixel_w,y*pixel_h,pixel_w,pixel_h))
	
def init_snake():
	pygame.init()

	display=pygame.display.set_mode((width,height),0,32)

	display.fill(black)	
	#Draw barrier
	for i in range(limit_barrier):
		pygame.draw.rect(display,white,(i*pixel_w,0,pixel_w,pixel_h))
		pygame.draw.rect(display,white,(0,i*pixel_h,pixel_w,pixel_h))
		pygame.draw.rect(display,white,((limit_barrier-1)*pixel_w,i*pixel_h,pixel_w,pixel_h))
		pygame.draw.rect(display,white,(i*pixel_w,(limit_barrier-1)*pixel_h,pixel_w,pixel_h))
		
	return display

def init_game(random):
	if(not random):
		display=init_snake()
	
	xposition = math.floor(limit_barrier/2)
	yposition = xposition
	
	#xposition = 1
	#yposition = 10
	
	velocity_p = 40000
	velocity = 0.1/velocity_p
	
	eat_points = 0
	#survive_points = eat_points/1000
	survive_points = 0
	explore_points = 0
	penalty_explore = 0
	#penalty_end_game = survive_points * limit_barrier * limit_barrier * 2
	penalty_end_game = -1
	
	if(random):
		predictor=None
	else:
		predictor= load('snake_model.joblib') 
	
	mySnake = snake(xposition,yposition,limit_barrier,eat_points,explore_points,survive_points,penalty_explore,penalty_end_game,[],random,predictor)

	#print(mySnake.score)	
	
	
	while mySnake.life==1:
		#time.sleep(velocity)
		mySnake.snake_random_movement()
		#mySnake.where_is()
		if(not random):
			erase_board(display)
			draw_pixel(display,mySnake.head[0],mySnake.head[1],mySnake.already_explored)

			#Events
			for event in pygame.event.get():
				if event.type==QUIT:
					pygame.quit()
					sys.exit()

			pygame.display.update()
		#print(mySnake.score)



	return mySnake.historial[-3:]
	#pd = pandas.DataFrame(mySnake.historial)
	#pd.to_csv("snake_data"+str(x)+".csv")

def generate_random_test():
	n_Test = 100000
	historical_data = []
	for x in range(n_Test):
		historical_data=historical_data+init_game(True)
		print(x)
		
		
	pd = pandas.DataFrame(historical_data)
	pd.to_csv("snake_data.csv")		
	
	#with open("snake_data.csv",'w') as f:
	#	for sublist in historical_data:
	#		for item in sublist:
	#			f.write(str(item) + ',')
	#		f.write('\n')
		


def test_snake_machine():
	for x in range(100):
		a = init_game(False)

import sys
def main():
	if(sys.argv[1]=="1"):
		generate_random_test()
	else:
		test_snake_machine()
main()
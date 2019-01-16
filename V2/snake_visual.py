import pygame,time,math
from snake_logic import snake
from pygame.locals import *
import numpy
import pandas
from joblib import dump, load

width = 500
height = 500

white=(255,255,255)
black=(0,0,0)
green=(0,255,0)
color=(255,0,0)

	
def draw_path_board(display,explored,lx,ly,pixel_h,pixel_w):
	for x in range(0,lx):
		for y in range(0,ly):
			if(explored[x][y]):
				pygame.draw.rect(display,green,(x*pixel_w,y*pixel_h,pixel_w,pixel_h))				
	
def draw_pixel(display,x,y,explored,lx,ly,pixel_h,pixel_w):
	#erase_board(display)
	draw_path_board(display,explored,lx,ly,pixel_h,pixel_w)
	pygame.draw.rect(display,white,(x*pixel_w,y*pixel_h,pixel_w,pixel_h))
	
	
def draw_map(display,map_1,lx,ly,pixel_h,pixel_w):
	for y in range(ly):
		for x in range(lx):
			if(map_1[x][y]==1):
				pygame.draw.rect(display,color,(y*pixel_h,x*pixel_w,pixel_w,pixel_h))
			else:
				pygame.draw.rect(display,black,(y*pixel_h,x*pixel_w,pixel_w,pixel_h))				

	
def init_snake():
	pygame.init()

	display=pygame.display.set_mode((width,height),0,32)

	display.fill(black)
	
	return display

def init_game(random,stop,visual,x_init=None,y_init=None):
	if(visual):
		display=init_snake()
	
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
	if(x_init==None or y_init==None):
		x_init = 15
		y_init = 15

		
	mySnake = snake(x_init,y_init,eat_points,explore_points,survive_points,penalty_explore,penalty_end_game,[],random,predictor,stop)
	limit_barrier_y = mySnake.limit_position_y
	limit_barrier_x = mySnake.limit_position_x
	
	pixel_w = width/limit_barrier_x
	pixel_h = height/limit_barrier_y

	while mySnake.life==1:
		#time.sleep(velocity)
		mySnake.snake_random_movement()
		#mySnake.where_is()
		if(visual):
			#erase_board(display)
			draw_map(display,mySnake.map,mySnake.limit_position_x,mySnake.limit_position_y,pixel_h,pixel_w)
			draw_pixel(display,mySnake.head[0],mySnake.head[1],mySnake.already_explored,mySnake.limit_position_x,mySnake.limit_position_y,pixel_h,pixel_w)

			#Events
			for event in pygame.event.get():
				if event.type==QUIT:
					pygame.quit()
					sys.exit()

			pygame.display.update()
		#print(mySnake.score)
	if(visual):
		pygame.quit()
	return mySnake.historial[-3:]
	#pd = pandas.DataFrame(mySnake.historial)
	#pd.to_csv("snake_data"+str(x)+".csv")

def generate_random_test(stop):
	#n_Test = 100000
	n_Test = 200000
	historical_data = []
	for x in range(n_Test):
		historical_data=historical_data+init_game(True,stop,False)
		print(x)
		
		
	pd = pandas.DataFrame(historical_data)
	pd.to_csv("snake_data.csv")		
	
	#with open("snake_data.csv",'w') as f:
	#	for sublist in historical_data:
	#		for item in sublist:
	#			f.write(str(item) + ',')
	#		f.write('\n')
		
def generate_learning_data(stop,n_test,visual,x_init,y_init):
	#n_Test = 100000
	historical_data = []
	print("HERE")
	for x in range(n_test):
		historical_data=historical_data+init_game(False,stop,visual,x_init,y_init)
		print(x)
		
	return historical_data
	#pd = pandas.DataFrame(historical_data)
	#pd.to_csv("snake_data.csv")		

def test_snake_machine(stop,number,x_init,y_init):
	for x in range(number):
		a = init_game(False,stop,True,x_init,y_init)



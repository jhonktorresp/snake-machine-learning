import random
import numpy
import random
import time

class snake:
	def __init__(self,startX,startY,limit_position,eat_points,explore_points,survive_points,penalty_explore_points,penalty_end_game,list_fruits_positions,random,predictor):
		self.head = [startX,startY]
		self.body = []
		self.direction = "up"
		self.direction_sum = [0,1]
		self.colision_proximity = False
		self.score = 0
		self.fruits_positions = list_fruits_positions
		self.options = [1,2,3]
		
		self.already_explored = numpy.full((limit_position, limit_position), False)
		
		self.life = 1
		
		self.random = random
		self.predictor = predictor
		
		#Score increments
		self.point_for_survive = survive_points
		self.point_for_eat = eat_points
		self.point_for_explore = explore_points
		self.penalty_explore = penalty_explore_points
		self.penalty_end_game = penalty_end_game
		

		
		#It will be from 0 to limit_position, SQUARE
		self.limit_position = limit_position
		
		self.historial = []
	
	def construct_step_historial(self,opt,pre_score):
		x = self.head[0]
		y = self.head[1]
		direccion = self.direction
		#Directions
		d1=0
		d2=0
		d3=0
		d4=0
		if(direccion=="up"):
			d1=1
		elif(direccion=="left"):
			d2=1
		elif(direccion=="down"):
			d3=1
		else:
			d4=1

		a1=0
		a2=0
		a3=0
		if(opt==1):
			a1=1
		elif(opt==2):
			a2=1
		elif(opt==3):
			a3=1
		
		score = self.score - pre_score
		
		#if(self.head[0]+self.direction_sum[0]<self.limit_position and self.head[0]+self.direction_sum[0]>=0 and self.head[1]+self.direction_sum[1]>=0 and self.head[1]+self.direction_sum[1]<self.limit_position ):
		#	next_explored = self.already_explored[self.head[0]+self.direction_sum[0]][self.head[1]+self.direction_sum[1]]
		#	if(next_explored):
		#		next_explored = 1
		#	else:
		#		next_explored = 0
		#else:
		#	next_explored = 0
			
		#decision_made = opt
		
		return [x,y,d1,d2,d3,d4,a1,a2,a3,score]
	
	def add_to_historial(self,opt,pre_score):
		self.historial.append(self.construct_step_historial(opt,pre_score))
	
	#Snake movement
	def turning_left(self): 
		if(self.direction=="up"):
			self.direction = "left"
			self.direction_sum = [-1,0]
		elif(self.direction=="left"):
			self.direction = "down"
			self.direction_sum = [0,-1]
		elif(self.direction=="right"):
			self.direction="up"
			self.direction_sum = [0,1]
		elif(self.direction=="down"):
			self.direction="right"
			self.direction_sum =[1,0]
	
	#Snake movement prediction
	def turning_left_prediction(self,d1,d2,d3,d4): 
		#d1: up
		#d2: left
		#d3: down
		#d4: right
		if(d1==1):
			return 0,1,0,0
		elif(d2==1):
			return 0,0,1,0
		elif(d3==1):
			return 0,0,0,1
		elif(d4==1):
			return 1,0,0,0

		
	def turning_rigth_prediction(self,d1,d2,d3,d4): 
		#d1: up
		#d2: left
		#d3: down
		#d4: right
		if(d1==1):
			return 0,0,0,1
		elif(d2==1):
			return 1,0,0,0
		elif(d3==1):
			return 0,1,0,0
		elif(d4==1):
			return 0,0,1,0
	
	def keep_forward(self):
		pass

	def score_for_survive(self):
		self.score+=self.point_for_survive		
	
	def score_for_explore(self):
		self.score+=self.point_for_explore
		
	def score_for_eat(self):
		self.score+=self.point_for_eat
		
	def score_end_penalty(self):
		self.score-=self.penalty_end_game
		
	def turning_right(self): 
		if(self.direction=="up"):
			self.direction = "right"
			self.direction_sum = [1,0]
		elif(self.direction=="left"):
			self.direction = "up"
			self.direction_sum = [0,1]
		elif(self.direction=="right"):
			self.direction="down"
			self.direction_sum = [0,-1]
		elif(self.direction=="down"):
			self.direction="left"
			self.direction_sum = [-1,0]	
			
	def check_collision(self):
		return self.head[0]<=0 or self.head[0]>=self.limit_position-1 or self.head[1]<=0 or self.head[1]>=self.limit_position-1
	
	def score_bad_explore(self):
		self.score -= self.penalty_explore
	
	#Snake step
	def one_step(self):
		self.head[0] += self.direction_sum[0]
		self.head[1] += self.direction_sum[1]	
		if(self.check_collision()):
			self.life = 0
			self.score_end_penalty()
			if(not self.random):
				time.sleep(2)
		else:
			self.score_for_survive()
			if(self.already_explored[self.head[0]][self.head[1]]):
				pass
				#self.score_bad_explore()
			else:
				self.already_explored[self.head[0]][self.head[1]] = True
				#self.score_for_explore()
			
	#Snake score
	def eat_fruit(self):
		self.score+=1
		
	def where_is(self):
		print(self.head)
	
	def prediction_movement(self):
		x = self.head[0]
		y = self.head[1]
		direccion = self.direction
		d1=0
		d2=0
		d3=0
		d4=0
		if(direccion=="up"):
			d1=1
		elif(direccion=="left"):
			d2=1
		elif(direccion=="down"):
			d3=1
		else:
			d4=1	
			
		a1=0
		a2=0
		a3=0	
		
		t1=False
		t2=False
		t3=False
		
		pre_d1_r,pre_d2_r,pre_d3_r,pre_d4_r = self.turning_rigth_prediction(d1,d2,d3,d4)
		pre_d1_l,pre_d2_l,pre_d3_l,pre_d4_l = self.turning_left_prediction(d1,d2,d3,d4)
		
		if(self.predictor.predict([[x+pre_d4_l-pre_d2_l,y+pre_d1_l-pre_d3_l,d1,d2,d3,d4,1,0,0]])[0]!=1):
			t1=True
		if(self.predictor.predict([[x+d4-d2,y+d1-d3,d1,d2,d3,d4,0,1,0]])[0]!=1):
			t2=True
		if(self.predictor.predict([[x+pre_d4_r-pre_d2_r,y+pre_d1_r-pre_d3_r,d1,d2,d3,d4,0,0,1]])[0]!=1):
			t3=True
		
		print(t1,x+pre_d4_l-pre_d2_l,y+pre_d1_l-pre_d3_l,d1,d2,d3,d4,1,0,0)
		print(t2,x+d4-d2,y+d1-d3,d1,d2,d3,d4,0,1,0)
		print(t3,x+pre_d4_r-pre_d2_r,y+pre_d1_r-pre_d3_r,d1,d2,d3,d4,0,0,1)
		print("----- INFO -^")
		#print([x+d4-d2,y+d1-d3,d1,d2,d3,d4,0,0,1])
		if(t1 and t2 and t3 ):
			return random.choice([1,2,3])
		elif(t1 and t2):
			return random.choice([1,2])
		elif(t1 and t3):
			return random.choice([1,3])
		elif(t2 and t3):
			return random.choice([2,3])
		elif(t1):
			return 1
		elif(t2):
			return 2
		elif(t3):
			return 3
		
		return 2
	
	def snake_random_movement(self):
		if(self.random):
			opt = random.sample(self.options, 1)[0]
		else:
			opt = self.prediction_movement()
		if(opt==1):
			self.turning_left()
		elif(opt==3):
			self.turning_right()
		pre_score = self.score
		self.one_step()
		self.add_to_historial(opt,pre_score)
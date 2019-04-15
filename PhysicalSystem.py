from tkinter import *
from random import *
from math import *

class Ball:
	ball_count = 0
	colors = ["red","green","yellow","blue", "hot pink", "turquoise", "orange", "purple", "white", "grey","brown"]
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.original_x = x
		self.original_y = y
		self.speed = 0
		self.x_direction = 1
		self.y_direction = 1
		self.color = Ball.colors[Ball.ball_count % len(Ball.colors)]
		self.radius = randint(5, 50)
		Ball.ball_count = Ball.ball_count + 1
	
	def getRadius(self):
		return self.radius
		
	def setX(self, x):
		self.x = x
		
	def getX(self):
		return self.x
	
	def setY(self, y):
		self.y = y
	
	def getY(self):
		return self.y
	
	def addY(self, y):
		self.y = self.y + y
	
	def addX(self, x):
		self.x = self.x + x
	
	def getColor(self):
		return self.color
	
	def setSpeed(self, speed):
		self.speed = speed
	
	def getSpeed(self):
		return self.speed
	
	def increment(self):   #check for ball collisions in here
		next_x = self.x + self.x_direction * self.speed
		next_y = self.y + self.y_direction * self.speed		
		if next_x < 0 or next_x > 1280:
			self.x_direction = -self.x_direction
			next_x = self.x + self.x_direction * self.speed
			
			
		if next_y < 0 or next_y > 600:
			self.y_direction = -self.y_direction
			next_y = self.y + self.y_direction * self.speed  #why is setting it as -next not work
		
		
		self.x = next_x
		self.y = next_y
	
	def setDirection(self):
		r = randint(0,1)
		if r == 0:
			self.x_direction = -1
		else:
			self.x_direction = 1
		r = randint(0,1)
		if r == 0:
			self.y_direction = -1
		else:
			self.y_direction = 1
	
	def getXDirection(self):
		return self.x_direction

	def getYDirection(self):
		return self.y_direction	
	
	def setXDirection(self, x):
		self.x_direction = x
		
	def setYDirection(self, y):
		self.x_direction = y

	def adjust_course(self, ball):
		next_y = self.y + self.y_direction * self.speed	
		next_x = self.x + self.x_direction * self.speed
		if next_x < ball.getX():
			self.x_direction  = -self.x_direction
			next_x = self.x + self.x_direction * self.speed
			
		if self.y < ball.getY():
			self.y_direction  = -self.y_direction
			next_y = self.y + self.y_direction * self.speed	
		self.x = next_x
		self.y = next_y
	
class BallSystem:
	def __init__(self):
		self.balls = []
		self.setBalls()
		self.setSpeed()
		self.setDirections()
		
	def setBalls(self):
		count = 0
		while count < 40:
			x = randint(0,1280)
			y = randint(0,600)
			away = True
			for i in range(len(self.balls)):
				if self.distance(self.balls[i], x, y) < 40:
					away = False
					break
			if away:
				self.balls.append(Ball(x,y))
				print("here")
				count = count + 1
					
	def distance(self, ball, x, y):
		return sqrt((x - ball.getX())**2 + (y - ball.getY())**2)
	
	def ball_distance(self, a, b):
		return sqrt(( a.getX()- b.getX())**2 + (a.getY() - b.getY())**2)
		
	def nextState(self):        #increments
		'''for i in range(len(self.balls)): implement physics
			ball1 = self.balls[i]
			for j in range(len(self.balls)):
				ball2 = self.balls[j]
				if i != j and self.ball_distance(ball1,ball2) < 40:
					ball1.adjust_course(ball2)
					ball2.adjust_course(ball1)
			self.balls[i].increment()'''
		for i in range(len(self.balls)):
			self.balls[i].increment()		
	
	def setSpeed(self):
		for ball in self.balls:
			ball.setSpeed(randint(2,20))
			
	def setDirections(self):
		for ball in self.balls:
			ball.setDirection()
			
	def getState(self):
		return self.balls



class View:
	def __init__(self, parent):
		self.parent = parent
		self.canvas1 = Canvas(parent, width = 1280, height = 600, bg = "black")
		self.canvas2 = Canvas(parent, width = 1280, height = 600, bg = "black")
		self.canvas1.grid(row = 0, column = 0)
		self.turn = True
	
	def draw(self, balls, canvas = None):
		if canvas == None:
			canvas = self.canvas1
		
		canvas.delete("all")
		for ball in balls:
			canvas.create_oval(ball.getX() - ball.getRadius(), ball.getY() - ball.getRadius(), \
			                         ball.getX() + ball.getRadius(), ball.getY() + ball.getRadius(), \
			            			 fill = ball.getColor())
	def drawState(self, balls):
		if self.turn:
			self.drawCanvas(balls, 1)
			self.canvas2.grid(row = 0, column = 0)
			self.canvas1.grid_forget()
		else:
			self.drawCanvas(balls, 2)
			self.canvas1.grid(row = 0, column = 0)
			self.canvas2.grid_forget()
		self.turn = not self.turn
		self.parent.update()
	
	def drawCanvas(self, balls, canvas):
		if canvas == 1:
			canvas = self.canvas2
		else:
			canvas = self.canvas1
		self.draw(balls, canvas)
		
	def getParent(self):
		return self.parent
		
class Controller:
	def __init__(self, view, model):
		self.model = model
		self.view = view
		self.setup()
	
	def setup(self):
		self.view.draw(self.model.getState())
		self.view.getParent().after(10, self.system_run)
	
	def system_run(self):
		self.model.nextState()
		self.view.drawState(self.model.getState())
		self.view.getParent().after(10, self.system_run)
		
		
				
		
class GUI:
	def __init__(self):
		window = Tk()
		Controller(View(window),BallSystem())
		window.mainloop()

GUI()
from random import choice
import sys
import tty
import termios
from threading import Thread
from time import sleep

class ball():
	
	direction_list = { "UPRIGHT":2,"DOWNRIGHT":4,"DOWNLEFT":6, "UPLEFT":8}

	def __init__(self):
		self.location = [5, 5]
		self.random_dir()



	def random_dir(self):
		self.direction = choice(list(self.direction_list.items()))[0]


	def move(self):
		#move up
		if self.direction_list[self.direction] in (2, 8):
			self.location[0] -= 1
			
		#move down
		if self.direction_list[self.direction] in (4, 6):
			self.location[0] += 1

		#move right
		if self.direction_list[self.direction] in (2, 4):
			self.location[1] += 1

		#move left
		if self.direction_list[self.direction] in (6, 8):
			self.location[1] -= 1


class paddle():
	location = [0,0]
	

	def __init__(self, y, x, height):
		self.location = [y, x]
		self.g_height = height

	def move_up(self):
		if self.location[0] > 2:
			self.location[0] -= 1


	def move_down(self):
		if self.location[0] < self.g_height-2:
			self.location[0] += 1


	def paddle_area(self):
		return [[self.location[0] -1, self.location[1]], [self.location[0], self.location[1]], [self.location[0]+1, self.location[1]]]
	
	
	
		


class game():
	def __init__(self, height, width):
		self.height = height
		self.width = width
		self.player1 = paddle(height//2, 0, height)
		self.player2 = paddle(height//2, width-1, height)
		self.cball = ball()
		self.quit = False


	def draw(self):
		print("\033c")
		_board = "|"
		
		for j in range(0 , self.height+1):
			for i in range(0, self.width):
				if [j ,i] == self.cball.location:
					_board +="O"
				elif j == 0:
					_board += "#"
				elif j == self.height:
					_board += "#"
				elif [j, i] in self.player1.paddle_area():
					_board += "x"
				elif [j, i] in self.player2.paddle_area():
					_board += "x"
				else:
					_board +=" "

			_board += "|\n|"
		print(_board)


	def input_dir(self):
		while(1):
			old_setting = termios.tcgetattr(sys.stdin)
			try:
				tty.setcbreak(sys.stdin.fileno())
				c = sys.stdin.read(3)
				if c == '\x1b[B':
					self.player1.move_down()
					self.player2.move_down()
				elif c == '\x1b[A':
					self.player1.move_up()
					self.player2.move_up()
				else:
					#TODO:
					pass
				self.draw()
			finally:
				termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_setting)

	def logic(self):
		if [self.cball.location[0], self.cball.location[1]-1] in self.player1.paddle_area():
			if self.cball.direction is "DOWNLEFT":
				self.cball.direction = "DOWNRIGHT"
			if self.cball.direction is "UPLEFT":
				self.cball.direction = "UPRIGHT"
		if [self.cball.location[0], self.cball.location[1]+1] in self.player2.paddle_area():
			if self.cball.direction is "DOWNRIGHT":
				self.cball.direction = "DOWNLEFT"
			if self.cball.direction is "UPRIGHT":
				self.cball.direction = "UPLEFT"


		if self.cball.location[0] <= 1:
			if self.cball.direction is "UPRIGHT":
				self.cball.direction = "DOWNRIGHT"
			if self.cball.direction is "UPLEFT":
				self.cball.direction = "DOWNLEFT"
				
				
		if self.cball.location[0] == self.height-1:
			if self.cball.direction is "DOWNRIGHT":
				self.cball.direction = "UPRIGHT"
			if self.cball.direction is "DOWNLEFT":
				self.cball.direction = "UPLEFT"
				
		if (self.cball.location[1] == -1 or
			self.cball.location[1] == self.width):
				self.quit = True
				
	def run_time(self):
			return 0.3;


	def run(self):
		thrd = Thread(target=self.input_dir)
		thrd.start()
		while(1):
			self.draw()
			self.cball.move()
			self.logic()
			#self.input_dir()
			sleep(self.run_time())
			if self.quit:
				print("(:")
				thrd.join()
				exit()	


if __name__ == "__main__":
	a = game(10,18)
	a.run()


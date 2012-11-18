from collections import deque

DIRECTION_UP = 1
DIRECTION_DOWN = 2
DIRECTION_LEFT = 3
DIRECTION_RIGHT = 4

class player:
#	def __init__(self):
#		self.snake = deque([[0, 0]])
#		self.direction = DIRECTION_DOWN
#	def __init__(self, x, y):
#		self.snake = deque([[x, y]])
#		self.direction = DIRECTION_DOWN
	def __init__(self, x, y, direction):
		self.snake = deque([[x, y]])
		self.direction = direction

	def append(self, coord):
		self.snake.append(coord)
	
	def popleft(self):
		return self.snake.popleft()

	def __getitem__(self, index):
		return self.snake[index]

	def __len__(self):
		return len(self.snake)

import curses
import time
from collections import deque

def main(scr):
	status = curses.newwin(1, curses.COLS, 0, 0) 
	status.bkgd('0')
	status.refresh()

	curses.start_color()
	debug = curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
	green = curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_GREEN)
	black = curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLACK)
	blue = curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLUE)
	debug = curses.color_pair(1)
	green = curses.color_pair(2)
	black = curses.color_pair(3)
	blue = curses.color_pair(4)

	DIRECTION_UP = 1
	DIRECTION_DOWN = 2
	DIRECTION_LEFT = 3
	DIRECTION_RIGHT = 4

	controlMapOne = {
	curses.KEY_UP:DIRECTION_UP, 
	curses.KEY_DOWN:DIRECTION_DOWN, 
	curses.KEY_LEFT:DIRECTION_LEFT, 
	curses.KEY_RIGHT:DIRECTION_RIGHT
	}
	controlMapTwo = {
	ord('w'):DIRECTION_UP,
	ord('s'):DIRECTION_DOWN,
	ord('a'):DIRECTION_LEFT,
	ord('d'):DIRECTION_RIGHT
	}

	curses.curs_set(False)
	scr.nodelay(True)

	tickDuration = 0.15
	playerOneCoord = deque([[29, 2]])
	playerTwoCoord = deque([[29, 30]])
	keypress = None
	currentDirectionOne = DIRECTION_UP
	currentDirectionTwo = DIRECTION_UP
	nextDirectionOne = DIRECTION_UP
	nextDirectionTwo = DIRECTION_UP

	draw(scr)
	drawPlayer(scr, playerOneCoord[0], green)
	drawPlayer(scr, playerTwoCoord[0], blue)
	previousTime = time.time()
	while True:
		if getDeltaTime(previousTime) >= tickDuration:
			playerOneCoord.append(movePlayer(scr, playerOneCoord[len(playerOneCoord)-1], green, nextDirectionOne, controlMapOne))
			playerTwoCoord.append(movePlayer(scr, playerTwoCoord[len(playerTwoCoord)-1], blue, nextDirectionTwo, controlMapTwo))
			if len(playerOneCoord) > 5:
				erasePlayer(scr, playerOneCoord.popleft(), black)
				erasePlayer(scr, playerTwoCoord.popleft(), black)
			previousTime = time.time()
			currentDirectionOne = nextDirectionOne
			currentDirectionTwo = nextDirectionTwo

		keypress = scr.getch()

		if keypress in (curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT):
			nextDirectionOne = getDirection(currentDirectionOne, keypress, controlMapOne)
		elif keypress in (ord('w'), ord('a'), ord('s'), ord('d')):
			nextDirectionTwo = getDirection(currentDirectionTwo, keypress, controlMapTwo)
		elif keypress == ord('p'):
			curses.delay_output(5000)
		elif keypress == ord('q'):
			break
		elif keypress == ord('r'):
			scr.clear()
			draw(scr)

def draw(scr):
	for x in xrange(0,80):
		y = 30
		scr.addstr(y, x, " ", curses.color_pair(1))

def getDeltaTime(previousTime):
	return time.time() - previousTime

def movePlayer(scr, coord, color, direction, controlMap):
	newCoord = list(coord)
	if direction == 1:
		newCoord[0] -= 1
	elif direction == 2:
		newCoord[0] += 1
	elif direction == 3:
		newCoord[1] -= 2
	elif direction == 4:
		newCoord[1] += 2
	drawPlayer(scr, coord, color)
	return newCoord

def erasePlayer(scr, coord, color):
	scr.addstr(coord[0], coord[1], ' ', color)
	scr.addstr(coord[0], coord[1]+1, ' ', color)

def drawPlayer(scr, coord, color):
	scr.addstr(coord[0], coord[1], ' ', color)
	scr.addstr(coord[0], coord[1]+1, ' ', color)

def getDirection(direction, keypress, controlMap):
	if direction in (1, 2):
		if controlMap[keypress] in (1, 2):
			return direction
	if direction in (3, 4):
		if controlMap[keypress] in (3, 4):
			return direction
	return controlMap[keypress]

curses.wrapper(main)

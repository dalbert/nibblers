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
	curses.curs_set(False)
	scr.nodelay(True)

	tickDuration = 0.15
	playerOneCoord = deque([[29, 2]])
	playerTwoCoord = deque([[29, 30]])
	keypress = None
	currentDirection = curses.KEY_UP
	nextDirection = curses.KEY_UP

	draw(scr)
	drawPlayer(scr, playerOneCoord[0], green)
	drawPlayer(scr, playerTwoCoord[0], blue)
	previousTime = time.time()
	while True:
		if getDeltaTime(previousTime) >= tickDuration:
			playerOneCoord.append(movePlayer(scr, playerOneCoord[len(playerOneCoord)-1], green, nextDirection))
			playerTwoCoord.append(movePlayer(scr, playerTwoCoord[len(playerTwoCoord)-1], blue, nextDirection))
			if len(playerOneCoord) > 5:
				erasePlayer(scr, playerOneCoord.popleft(), black)
				erasePlayer(scr, playerTwoCoord.popleft(), black)
			previousTime = time.time()
			currentDirection = nextDirection

		keypress = scr.getch()

		if keypress in (curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT):
			nextDirection = getDirection(currentDirection, keypress)
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

def movePlayer(scr, coord, color, direction):
	newCoord = list(coord)
	if direction == curses.KEY_UP:
		newCoord[0] -= 1
	elif direction == curses.KEY_DOWN:
		newCoord[0] += 1
	elif direction == curses.KEY_LEFT:
		newCoord[1] -= 2
	elif direction == curses.KEY_RIGHT:
		newCoord[1] += 2
	drawPlayer(scr, coord, color)
	return newCoord

def erasePlayer(scr, coord, color):
	scr.addstr(coord[0], coord[1], ' ', color)
	scr.addstr(coord[0], coord[1]+1, ' ', color)

def drawPlayer(scr, coord, color):
	scr.addstr(coord[0], coord[1], ' ', color)
	scr.addstr(coord[0], coord[1]+1, ' ', color)

def getDirection(direction, keypress):
	if direction in (curses.KEY_UP, curses.KEY_DOWN):
		if keypress in (curses.KEY_UP, curses.KEY_DOWN):
			return direction
	if direction in (curses.KEY_LEFT, curses.KEY_RIGHT):
		if keypress in (curses.KEY_LEFT, curses.KEY_RIGHT):
			return direction
	return keypress

curses.wrapper(main)

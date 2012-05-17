import curses
import time

def main(scr):
	status = curses.newwin(1, curses.COLS, 0, 0) 
	status.bkgd('0')
	status.refresh()

	curses.start_color()
	curses.init_pair(1, curses.COLOR_RED, curses.COLOR_RED)
	curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_GREEN)
	curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLACK)
	curses.curs_set(False)
	scr.nodelay(True)

	tickDuration = 0.25
	playerCoord = [29, 2]
	keypress = None
	currentDirection = curses.KEY_UP
	nextDirection = curses.KEY_UP

	draw(scr)
	drawPlayer(scr, playerCoord)
	previousTime = time.time()
	while True:
		if getDeltaTime(previousTime) >= tickDuration:
			playerCoord = movePlayer(scr, playerCoord, nextDirection)
			previousTime = time.time()
			currentDirection = nextDirection

		keypress = scr.getch()

		if keypress in (curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT):
			nextDirection = getDirection(currentDirection, keypress)
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

def movePlayer(scr, coord, direction):
	erasePlayer(scr, coord)
	if direction == curses.KEY_UP:
		coord[0] -= 1
	elif direction == curses.KEY_DOWN:
		coord[0] += 1
	elif direction == curses.KEY_LEFT:
		coord[1] -= 2
	elif direction == curses.KEY_RIGHT:
		coord[1] += 2
	drawPlayer(scr, coord)
	return coord

def erasePlayer(scr, coord):
	scr.addstr(coord[0], coord[1], ' ', curses.color_pair(3))
	scr.addstr(coord[0], coord[1]+1, ' ', curses.color_pair(3))

def drawPlayer(scr, coord):
	scr.addstr(coord[0], coord[1], ' ', curses.color_pair(2))
	scr.addstr(coord[0], coord[1]+1, ' ', curses.color_pair(2))

def getDirection(direction, keypress):
	if direction in (curses.KEY_UP, curses.KEY_DOWN):
		if keypress in (curses.KEY_UP, curses.KEY_DOWN):
			return direction
	if direction in (curses.KEY_LEFT, curses.KEY_RIGHT):
		if keypress in (curses.KEY_LEFT, curses.KEY_RIGHT):
			return direction
	return keypress

curses.wrapper(main)

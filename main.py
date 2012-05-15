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

	tickDuration = 0.5
	playerCoord = [29, 2]
	keypress = None

	draw(scr)
	previousTime = time.time()
	while True:
		if getDeltaTime(previousTime) >= tickDuration:
			scr.addstr(0, 0, str(time.time()), curses.color_pair(2))
			if keypress in (curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT):
				playerCoord = movePlayer(scr, playerCoord, keypress)
				previousTime = time.time()

		keypress = scr.getch()
		
		if keypress == ord('q'):
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
	scr.delch(coord[0], coord[1])
	if direction == curses.KEY_UP:
		coord[0] -= 1
	elif direction == curses.KEY_DOWN:
		coord[0] += 1
	elif direction == curses.KEY_LEFT:
		coord[1] -= 1
	elif direction == curses.KEY_RIGHT:
		coord[1] += 1
	scr.addstr(coord[0], coord[1], ' ', curses.color_pair(2))
	return coord


curses.wrapper(main)

from cppgen import *
import curses
from curses.textpad import Textbox

up_chars = ""

stdscr = curses.initscr()
curses.start_color()
curses.noecho()
curses.cbreak()

curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_WHITE)

display_win = curses.newwin(curses.LINES-2,curses.COLS,0,0)
input_win = curses.newwin(2,curses.COLS,curses.LINES-2,0)
stdscr.move(curses.LINES-1,2)

divider = ""
for i in range(0,curses.COLS):
    divider += '-'

classes = []
class_index = 0

def get_input():
    input_win.clear()
    input_win.refresh()
    curses.echo()
    s = input_win.getstr(0,0,255)
    curses.noecho()
    input_win.clear()
    input_win.refresh()
    return s

def display_curr_class():
    display_win.move(0,0)
    display_win.clear()
    dpstr = classes[class_index].as_header_str()
    display_win.addstr(0,0,dpstr)
    display_win.refresh()





running = True
while running:
    cmd = get_input().decode('utf-8')
    cmd = cmd.split(' ')
    if cmd[0] == "quit":
        running = False
    elif cmd[0] == "new":
        if len(cmd) == 3:
            classes.append(cpp_class(cmd[1],cmd[2]))
        elif len(cmd) == 2:
            classes.append(cpp_class(cmd[1]))
    elif cmd[0] == "av":
        if len(cmd) == 3:
            var = cpp_var(cmd[1],cmd[2])
            


    if len(classes) > 0:
        display_curr_class()
    # display_win.refresh()
    # stdscr.refresh()

    
    

curses.echo()
curses.endwin()
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

def display_curr_class(showSource):
    display_win.move(0,0)
    display_win.clear()
    if showSource:
        dpstr = classes[class_index].as_source_str()
    else:
        dpstr = classes[class_index].as_header_str()
    display_win.addstr(0,0,dpstr)
    display_win.refresh()

def display_warning(warning):
    display_win.move(0,0)
    display_win.clear()
    display_win.addstr(0,0,warning)
    display_win.refresh()
    



showSource = False

running = True
while running:
    warn = ""
    cmd = get_input().decode('utf-8')
    cmd = cmd.split(' ')
    if cmd[0] == "quit":
        running = False
    elif cmd[0] == "new":
        if len(cmd) == 3:
            classes.append(cpp_class(cmd[1],cmd[2]))
        elif len(cmd) == 2:
            classes.append(cpp_class(cmd[1]))
    elif cmd[0] == "av" or cmd[0] == "add-var":
        if len(cmd) == 3:
            var = cpp_var(cmd[1],cmd[2])
            classes[class_index].add_var(var,False,False)
        if len(cmd) > 3:
            var = cpp_var(cmd[1],cmd[2])
            genset = False
            genget = False
            for x in range(3,len(cmd)):
                if cmd[x] == "-gs" or cmd[x] == "--gen-setter":
                    genset = True
                elif cmd[x] == "-gg" or cmd[x] == "--gen-getter":
                    genget = True
                    
            classes[class_index].add_var(var,genget,genset)
    elif cmd[0] == "export":
        for cl in classes:
            with open(cl.name+".hpp",'w') as header:
                header.write(cl.as_header_str())
            with open(cl.name+".cpp",'w') as source:
                source.write(cl.as_source_str())
    elif cmd[0] == "source":
        showSource = True
    elif cmd[0] == "header":
        showSource = False
            

    # elif cmd[0] == "am" or cmd[0] == "add-method"
            

    if warn != "":
        display_warning(warn)
    elif len(classes) > 0:
        display_curr_class(showSource)
    # display_win.refresh()
    # stdscr.refresh()

    
    

curses.echo()
curses.endwin()
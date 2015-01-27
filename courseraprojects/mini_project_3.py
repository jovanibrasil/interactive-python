import simplegui
import time

# define global variables

global counter
global str_timer
global a, b, c, d
global points, attempts
global state

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D

def format(t):
    global str_timer, a, b, c, d   
    a = str(t//600)
    b = str((t / 10) % 60 / 10)
    c = str((t / 10) % 10)
    d = str(t % 10)  
    str_timer = str(a) + ":" + str(b) + str (c) + "." + str(d)
    
# define event handlers for buttons; "Start", "Stop", "Reset"

def start():
    global timer, state
    timer.start()
    state = False
    
def stop():
    global state, timer, b, c, d, points, attempts
    if state == False:
        state = True
        timer.stop()
        if d == "0":
            points += 1
        attempts+= 1
    
    
def reset():
    global state, timer, counter, str_timer, points, attempts
    counter = attempts = points = 0
    str_timer = "0:00.0"
    timer.stop()
    state = False

    
# define event handler for timer with 0.1 sec interval

def update_timer():
    global counter
    counter+=1
    format(counter)

# define draw handler

def draw(canvas):
    canvas.draw_text(str_timer, [120,170], 60, "White")
    s = str(points) + "/" + str(attempts)
    canvas.draw_text(s, [330,50], 25, "Green")
    
# create frame

frame = simplegui.create_frame("Stop Watch", 400, 300)

# register event handlers

str_timer = "0:00.0"
a = b = c = d = "0"
state = False
points = counter = attempts = 0
btn_start = frame.add_button("Start", start, 150)
btn_stop = frame.add_button("Stop", stop, 150)
btn_reset = frame.add_button("Reset", reset, 150)

frame.set_draw_handler(draw)
timer = simplegui.create_timer(100, update_timer)

# start frame
frame.start()

# Please remember to review the grading rubric

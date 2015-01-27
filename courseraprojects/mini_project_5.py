# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals
def new_game():
    global cards, cards_state, choice, state, turns
    state = 0
    turns = 0
    choice = []
    cards = []
    cards_state = []
    for value in range(8):
        cards.extend([value, value])
        cards_state.extend([False, False])     
    random.shuffle(cards)
        
# define event handlers
def mouseclick(pos):
    global cards, turns, cards_state, choice, state
    border = 50
        
    for value in range(16):
        if(pos[0] < border and pos[0] > border-50):
            if cards_state[value] == True:
                return
            turns+=1
            if state == 0:
                state = 1
            elif state == 1:
                state = 2
            else:
                state = 1
                if cards[choice[0]] != cards[choice[1]]:
                    cards_state[choice[0]] = False
                    cards_state[choice[1]] = False
                choice = []
            choice.append(value)
            cards_state[value] = True
                          
        border += 50
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global cards, cards_state, turns
    border = 50
    canvas.draw_line((1, 0), (1, 100), 3, "White")
    for value in range(16):
        if cards_state[value] is True:
            canvas.draw_polygon([(border-48,0),(border-48,100),(border-2,100), (border-2,0)], 2,"White","White")
            canvas.draw_text(str(cards[value]), (border - 35, 65), 40, "Black")
        else:
            canvas.draw_polygon([(border-48,0),(border-48,100),(border-2,100), (border-2,0)], 2,"Green","Green")
            canvas.draw_line((border, 0), (border, 100), 3, "White")
            canvas.draw_line((border, 1), (border-50, 1), 3, "White")
            canvas.draw_line((border, 99), (border-50, 99), 3, "White")
        border += 50
    label.set_text("Turns = "+ str(turns))
    
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

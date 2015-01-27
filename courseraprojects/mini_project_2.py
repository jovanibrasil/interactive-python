import simplegui
import random
import math

high = 100

def new_game():
    """initialize global variables"""
    global int_guess, secret_number, high, guesses
    secret_number = random.randrange(0,high)
    int_guess = 0
    guesses = int(math.ceil((math.log(high - 0 + 1))/(math.log(2))))
    print "New game. Range is from 0 to", high
    print "Number of remaining guesses is", guesses
    
def range100():
    """ button that changes the range to [0,100) and starts a new game"""
    global int_guess, secret_number, high
    high = 100
    print ""
    new_game()
    
def range1000():
    """ button that changes the range to [0,1000) and starts a new game"""     
    global int_guess, secret_number, high
    high = 1000
    secret_number = random.randrange(0,1000)
    print ""
    new_game()
    
def input_guess(guess):
    """ main game logic here """
    global int_guess, secret_number, guesses
    int_guess = int(guess)
    print "\nGuess was", guess
    guesses -= 1
    print "Number of remaining guesses is", guesses
    
    if int_guess == secret_number:
        print "Correct!\n"
        new_game()      
    if guesses == 0:
        print "You ran out of guesses.  The number was", secret_number, "\n"
        new_game() 
    elif int_guess < secret_number:
        print "Higher!"
    else:
        print "Lower!"
        
# create frame
# register event handlers for control elements and start frame
f = simplegui.create_frame("Guess the Number", 100, 200)
f.add_input("Enter", input_guess ,100)
f.add_button("Range 100", range100, 100)
f.add_button("Range 1000", range1000, 100)
f.start()
# call new_game 
new_game()

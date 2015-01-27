# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
            self.is_first = False
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank
    
    def set_first(self, value):
        self.is_first = value
    
    def draw(self, canvas, pos):
        
        if self.is_first is True:
            images = card_back
            card_loc = (CARD_BACK_CENTER[0] ,CARD_BACK_CENTER[1])
        else:
            images = card_images
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
            
        canvas.draw_image(images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []
        
    def __str__(self):
        s = "Hand contains"
        for card in self.hand:
            s += " " + str(card)
        return s

    def add_card(self, card):
        if self.hand == []:
             self.first = True
        self.hand.append(card)

    def get_value(self):
        value = 0
        for card in self.hand:
            value += VALUES[card.get_rank()]
        return value
    
    def draw(self, canvas, pos):
        offset = 50
        for card in self.hand:
            card.draw(canvas, [pos[0]+offset, pos[1]])
            offset+=80
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS: 
            for rank in RANKS:
                self.deck.append(Card(suit,rank))
    
    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()
    
    def __str__(self):
        s = "Deck contains"
        for card in self.deck:
            s += " " + str(card)
        return s

#define event handlers for buttons
def deal():
    global outcome, deck, in_play, dealer_hand, player_hand, outcome, score
    deck = Deck()
    deck.shuffle()
   
    if in_play == True:
        score -= 1
    
    player_hand = Hand()
    dealer_hand = Hand()
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    d = deck.deal_card()
    d.set_first(True)
    dealer_hand.add_card(d)
    dealer_hand.add_card(deck.deal_card())
    
    in_play = True
    outcome = "Hit or stand?"
    
def hit():
    # if the hand is in play, hit the player
    global in_play, score, outcome
    if in_play == True:
        player_hand.add_card(deck.deal_card())
        outcome = "Hit or stand?"
        # if busted, assign a message to outcome, update in_play and score
        if player_hand.get_value() > 21 or in_play == False:
            dealer_hand.hand[0].set_first(False)
            in_play = False
            score -= 1
            outcome = "You have busted! New deal?"
            print player_hand.get_value()
            print dealer_hand.get_value()
            
def stand():
    global dealer_hand, player_hand, deck, in_play, score, outcome
    dealer_hand.hand[0].set_first(False)
    if in_play == True:
        # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
        while dealer_hand.get_value() <= 17:
            dealer_hand.add_card(deck.deal_card())
        # assign a message to outcome, update in_play and score
        if dealer_hand.get_value() > 21:
            outcome = "You win! New deal?"
            score += 1
            in_play = False
        else:
            in_play = False
            if player_hand.get_value() < dealer_hand.get_value():
                outcome = "You have Busted! New deal?"
                score -= 1
            else:
                score += 1
                outcome = "You win! New deal?"
    
# draw handler    
def draw(canvas):
    global dealer_hand, player_hand, player_score, outcome
    canvas.draw_text("Black Jack",[50,100], 50, "Black")
    canvas.draw_text("Dealer",[50,200], 25, "Black")
    canvas.draw_text("Player",[50,400], 25, "Black")
    canvas.draw_text("Score: "+str(score),[500,20], 25, "Black")
    canvas.draw_text(outcome,[300,400], 25, "Black")
    dealer_hand.draw(canvas, [0,210])
    player_hand.draw(canvas, [0,410])
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()

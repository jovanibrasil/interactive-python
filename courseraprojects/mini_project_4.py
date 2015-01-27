# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
score_left = 0
score_right = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel
    global paddle1_vel, paddle2_vel, paddle2_pos, paddle1_pos
    ball_pos = [WIDTH/2, HEIGHT/2]
    if direction == RIGHT:
        ball_vel = [random.randrange(2, 3),(-random.randrange(2, 3))]
    elif direction == LEFT:
        ball_vel = [-random.randrange(2, 3),(-random.randrange(2, 3))]
    
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    paddle2_pos = HEIGHT/2
    paddle1_pos = HEIGHT/2
    paddle1_vel = 0
    paddle2_vel = 0
    direction = random.choice([LEFT,RIGHT])
    spawn_ball(direction)
    
def pad_collision(position):
    
    if position + BALL_RADIUS > paddle2_pos - HALF_PAD_HEIGHT:
        if position < paddle2_pos + HALF_PAD_HEIGHT:
            return True
    elif position - BALL_RADIUS < paddle2_pos + HALF_PAD_HEIGHT:
        if position > paddle2_pos - HALF_PAD_HEIGHT:
            return True
    if position + BALL_RADIUS > paddle1_pos - HALF_PAD_HEIGHT:
        if position < paddle1_pos + HALF_PAD_HEIGHT:
            return True
    elif position - BALL_RADIUS < paddle1_pos + HALF_PAD_HEIGHT:
        if position > paddle1_pos - HALF_PAD_HEIGHT:
            return True
    return False
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, score_left, score_right
 
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    if ball_pos[0] + ball_vel[0] > WIDTH - PAD_WIDTH - BALL_RADIUS:
        if pad_collision(ball_pos[1]) == False:
            score_left +=1
            spawn_ball(LEFT)
            return
        ball_vel[0] *=-1 * 1.1
    if ball_pos[0] + ball_vel[0] < BALL_RADIUS + PAD_WIDTH:
        if pad_collision(ball_pos[1]) == False:
            score_right +=1
            spawn_ball(RIGHT)
            return
        ball_vel[0] *=-1 * 1.1
    if ball_pos[1] + ball_vel[1] < BALL_RADIUS:
        ball_vel[1] *=-1
    if ball_pos[1] + ball_vel[1] + BALL_RADIUS == HEIGHT:
        ball_vel[1] *=-1
    
    
    ball_pos[1] += ball_vel[1]
    ball_pos[0] += ball_vel[0]    
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos - HALF_PAD_HEIGHT + paddle1_vel > 0 and paddle1_pos - HALF_PAD_HEIGHT + paddle1_vel < HEIGHT - PAD_HEIGHT:
        paddle1_pos += paddle1_vel
    if paddle2_pos - HALF_PAD_HEIGHT + paddle2_vel > 0 and paddle2_pos - HALF_PAD_HEIGHT + paddle2_vel < HEIGHT - PAD_HEIGHT:
        paddle2_pos += paddle2_vel
    a = [0, paddle1_pos - HALF_PAD_HEIGHT]
    b = [PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT]
    c = [PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT]
    d = [0, paddle1_pos + HALF_PAD_HEIGHT]
    # draw paddles
    canvas.draw_polygon([a, b, c, d], 1, 'white', 'white')
    a = [WIDTH - PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT]
    b = [WIDTH, paddle2_pos - HALF_PAD_HEIGHT]
    c = [WIDTH, paddle2_pos + HALF_PAD_HEIGHT]
    d = [WIDTH - PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT]
    canvas.draw_polygon([a, b, c, d], 1, 'white', 'white')
    
    # draw scores
    canvas.draw_text(str(score_left), [150, 100], 50, "White")
    canvas.draw_text(str(score_right), [450, 100], 50, "White")
    
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = -2
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = 2
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 2
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = -2
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    paddle1_vel = 0
    paddle2_vel = 0
    
def restart():
    global score_right, score_left
    score_right = 0
    score_left = 0
    new_game()


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", restart,100)

# start frame
new_game()
frame.start()

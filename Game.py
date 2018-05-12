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
# variables that I initialized
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0, 0]
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0
# initialize ball_pos and ball_vel for new ball in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_vel[0] = random.randrange(120, 240) / 60.0
    ball_vel[1] = -random.randrange(60, 180) / 60.0
    ball_pos[0] = WIDTH / 2
    ball_pos[1] = HEIGHT / 2
    if direction == False:
        ball_vel[0] = -ball_vel[0] 

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    x = random.randrange(0,2)
    if x == 0:
        spawn_ball(RIGHT)
    else:
        spawn_ball(LEFT)
    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel     
    # keeps the ball from going out of upper and lower limits of canvas
    if ball_pos[1] >= (HEIGHT - BALL_RADIUS) or ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]       
    
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 4, "Purple")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "Yellow")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "Yellow")
    canvas.draw_circle([WIDTH / 2, HEIGHT / 2], 85, 4, "Purple")
        
    # update ball
    ball_pos = [ball_pos[0] + ball_vel[0], ball_pos[1] + ball_vel[1]] 
    
    # draw ball    
    canvas.draw_circle(ball_pos, BALL_RADIUS - 2, 13, "Purple") # makes a purple ring
    canvas.draw_circle(ball_pos, BALL_RADIUS - 2, 7, "White")   # makes a white ring   
    
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos + paddle1_vel >= HALF_PAD_HEIGHT and paddle1_pos + paddle1_vel <= HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos += paddle1_vel
    else:
        paddle1_vel = 0    
    if paddle2_pos + paddle2_vel >= HALF_PAD_HEIGHT and paddle2_pos + paddle2_vel <= HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos += paddle2_vel
    else:
        paddle2_vel = 0    
    
    # draw paddles
    canvas.draw_line([HALF_PAD_WIDTH, (paddle1_pos + HALF_PAD_HEIGHT)], [HALF_PAD_WIDTH, (paddle1_pos - HALF_PAD_HEIGHT)], PAD_WIDTH, "Red")
    canvas.draw_line([(WIDTH - HALF_PAD_WIDTH), (paddle2_pos + HALF_PAD_HEIGHT)], [(WIDTH - HALF_PAD_WIDTH), (paddle2_pos - HALF_PAD_HEIGHT)], PAD_WIDTH, "Lime")
    
    # determine whether paddle and ball collide AND if ball goes into the gutters
    # If ball goes in gutters: respawn accordingly. If ball hits paddle, reflect ball's horizontal position
    if ball_pos[0] - (BALL_RADIUS + PAD_WIDTH) <= 0:
        if ball_pos[1] < paddle1_pos + HALF_PAD_HEIGHT and ball_pos[1] > paddle1_pos - HALF_PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] += 0.1 * ball_vel[0] # increasing speed by 10% after each successfull reflection
            ball_vel[1] += 0.1 * ball_vel[1] # increasing speed by 10% after each successfull reflection            
        else:
            spawn_ball(RIGHT)
            score2 += 1
    elif ball_pos[0] + (BALL_RADIUS + PAD_WIDTH) >= WIDTH:
        if ball_pos[1] < paddle2_pos + HALF_PAD_HEIGHT and ball_pos[1] > paddle2_pos - HALF_PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] += 0.1 * ball_vel[0]  # increasing speed by 10% after each successfull reflection
            ball_vel[1] += 0.1 * ball_vel[1]  # increasing speed by 10% after each successfull reflection            
        else:
            spawn_ball(LEFT)  
            score1 += 1
            
    # draw score
    canvas.draw_text(str(score1), [180, 50], 55, "Red") # left player score
    canvas.draw_text(str(score2), [420, 50], 55, "Lime") # right player score
    
def keydown(key):
    global paddle1_vel, paddle2_vel    
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = -10             
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = 10   
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel = -10        
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 10
    
def keyup(key):
    global paddle1_vel, paddle2_vel    
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = 0 
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0 
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = 0        
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0
def paddle(key):
    pass
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game, 100)
frame.add_button("W and S for left paddles. Up and Down arrow for right paddle", paddle, 200)
# start frame
new_game()
frame.start()







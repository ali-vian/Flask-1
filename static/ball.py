from vpython import *
import random

# Set up the scene
scene = canvas(width=800, height=600)

# Create the walls of the box
L = 7
wall_right = box(pos=vector(L, 0, 0), size=vector(0.1, 2*L, 2*L), color=color.white)
wall_left = box(pos=vector(-L, 0, 0), size=vector(0.1, 2*L, 2*L), color=color.white)
wall_top = box(pos=vector(0, L, 0), size=vector(2*L, 0.1, 2*L), color=color.white)
wall_bottom = box(pos=vector(0, -L, 0), size=vector(2*L, 0.1, 2*L), color=color.white)
wall_back = box(pos=vector(0, 0, -L), size=vector(2*L, 2*L, 0.1), color=color.white)

# Function to generate random positions ensuring no overlap
def generate_random_position(existing_positions, ball_radius):
    while True:
        pos = vector(random.uniform(-L+1, L-1), random.uniform(-L+1, L-1), 0)
        if all(mag(pos - p) > 2*ball_radius for p in existing_positions):
            return pos

# Create balls with different colors
colors = [color.red, color.green, color.blue, color.yellow, color.orange]
balls = []
ball_radius = 0.6
positions = []

for i in range(5):
    pos = generate_random_position(positions, ball_radius)
    positions.append(pos)
    balls.append(sphere(pos=pos,
                        radius=ball_radius, color=colors[i],
                        velocity=vector(random.uniform(-1, 1), random.uniform(-1, 1), 0),
                        stopped=False))

# Create the purple ball
purple_ball = sphere(pos=vector(0, 0, 0), radius=ball_radius, color=color.purple, velocity=vector(0, 0, 0))

# Set up text for collision count
collision_count = 0
collision_text = label(pos=vector(0, L+1, 0), text='Score: 0', color=color.yellow, height=20, box=False,opacity=0)
win_text = label(pos=vector(0, 0, 0), text='You Win!', color=color.green, height=50, box=False)
win_text.visible = False

# Define control modes
bounce_mode = True
game_started = False

# Define button function
def toggle_mode():
    global bounce_mode
    bounce_mode = not bounce_mode
    mode_button.text = 'Mode: Bounce' if bounce_mode else 'Mode: Stop'

# Create buttons
mode_button = button(text='Mode: Bounce', bind=toggle_mode, pos=scene.title_anchor)

def start_game():
    global game_started, collision_count
    game_started = True
    collision_count = 0
    collision_text.text = 'Score: 0'
    win_text.visible = False
    start_button.disabled = True

def restart_game():
    start_game()
    for ball in balls:
        ball.pos = generate_random_position([b.pos for b in balls], ball_radius)
        ball.velocity = vector(random.uniform(-1, 1), random.uniform(-1, 1), 0)
        ball.stopped = False
    purple_ball.pos = vector(0, 0, 0)
    purple_ball.velocity = vector(0, 0, 0)
    restart_button.disabled = True

start_button = button(text='Start Game', bind=start_game ,pos=scene.title_anchor)
restart_button = button(text='Restart Game', bind=restart_game, pos=scene.title_anchor, disabled=True)

# Define keyboard controls for the purple ball
def move_purple_ball(evt):
    s = evt.key
    if s == 'left' or s == 'a' or s == 'A':
        purple_ball.velocity.x = -1
    elif s == 'right' or  s == 'd' or s == 'D':
        purple_ball.velocity.x = 1
    elif s == 'up' or s == 'w' or s == 'W':
        purple_ball.velocity.y = 1
    elif s == 'down'  or s == 's' or s == 'S':
        purple_ball.velocity.y = -1

scene.bind('keydown', move_purple_ball)

# Update function
def update_positions():
    global collision_count

    # Update position of balls
    for ball in balls:
        ball.pos += ball.velocity * dt

        # Check for collisions with walls
        if ball.pos.x > L-ball_radius or ball.pos.x < -L+ball_radius:
            ball.velocity.x *= -1
        if ball.pos.y > L-ball_radius or ball.pos.y < -L+ball_radius:
            ball.velocity.y *= -1

        # Check for collisions with other balls
        for other in balls:
            if ball != other and mag(ball.pos - other.pos) < 2*ball_radius:
                ball.velocity, other.velocity = other.velocity, ball.velocity

        # Check for collision with purple ball
        if mag(ball.pos - purple_ball.pos) < 2*ball_radius:
            if bounce_mode:
                ball.velocity, purple_ball.velocity = purple_ball.velocity, ball.velocity
                collision_count += 1
                collision_text.text = f'Score: {collision_count}'
            else:
                if not ball.stopped:
                    ball.velocity = vector(0, 0, 0)
                    collision_count += 1
                    collision_text.text = f'Score: {collision_count}'
                    ball.stopped = True
        else:
            ball.stopped = False

    # Update position of purple ball
    purple_ball.pos += purple_ball.velocity * dt

    # Check for collisions with walls for purple ball
    if purple_ball.pos.x > L-ball_radius or purple_ball.pos.x < -L+ball_radius:
        purple_ball.velocity.x *= -1
    if purple_ball.pos.y > L-ball_radius or purple_ball.pos.y < -L+ball_radius:
        purple_ball.velocity.y *= -1

    # Check for win condition
    if collision_count >= 30:
        win_text.visible = True
        restart_button.disabled = False

# Time step
dt = 0.02

# Main loop
while True:
    rate(100)
    if game_started:
        update_positions()

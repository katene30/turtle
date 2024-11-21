import pygame
import sys
import random
import math
from seaweed import Seaweed  # Import the Seaweed class from seaweed.py
from score import Score

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Turtle Desktop Buddy")

# Load Turtle Idle Animation Frames
idle_frames = []
colorkey = (0, 0, 0)  # Set to the background color in your images

for i in range(0, 4):  # Assuming files are named idle_turtle_0.png to idle_turtle_3.png
    frame = pygame.image.load(f"assets/idle_turtle{i}.png").convert_alpha()
    frame.set_colorkey(colorkey)
    scaled_width = frame.get_width() * 4  # Scale the frame (4x size)
    scaled_height = frame.get_height() * 4
    scaled_frame = pygame.transform.scale(frame, (scaled_width, scaled_height))
    idle_frames.append(scaled_frame)

# Load Sleeping Animation Frames
sleeping_frames = []
for i in range(0, 4):  # Assuming files are named sleep_turtle_0.png to sleep_turtle_3.png
    frame = pygame.image.load(f"assets/sleep_turtle{i}.png").convert_alpha()
    frame.set_colorkey(colorkey)
    scaled_width = frame.get_width() * 4  # Scale the frame (4x size)
    scaled_height = frame.get_height() * 4
    scaled_frame = pygame.transform.scale(frame, (scaled_width, scaled_height))
    sleeping_frames.append(scaled_frame)

# Load Walking Animation Frames
walking_frames = []
for i in range(0, 4):  # Assuming files are named turtle_walk0.png to turtle_walk3.png
    frame = pygame.image.load(f"assets/turtle_walk{i}.png").convert_alpha()
    frame.set_colorkey(colorkey)
    scaled_width = frame.get_width() * 4  # Scale the frame (4x size)
    scaled_height = frame.get_height() * 4
    scaled_frame = pygame.transform.scale(frame, (scaled_width, scaled_height))
    walking_frames.append(scaled_frame)

# Animation variables
current_frame = 0
frame_timer = 0
frame_delay = 150  # Delay between frames in milliseconds
state = "idle"  # Initialize state

# Position and movement variables
turtle_rect = idle_frames[0].get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
facing_left = False  # Tracks if the turtle is facing left
speed = 2  # Pixels per frame

# Seaweed list to store seaweed instances
seaweed_list = []

# Score variable
score = Score() # Initialize score

# Eating delay variables
eat_delay = 1000  # 1 second delay when eating seaweed (in milliseconds)
eat_timer = 0  # Timer to track eating delay

# Clock for controlling the game loop
clock = pygame.time.Clock()

# Define turtle states
sleeping = False
eating_seaweed = None  # Track the seaweed currently being eaten
idle_time = 0  # Time the turtle has been idle (in milliseconds)
idle_threshold = 5000  # 5 seconds of inactivity


def move_toward_target(rect, target, speed, head_offset=50):
    """
    Move the turtle rect toward the target position at the given speed.
    Stops when within the offset radius from the target.
    """
    dx, dy = target[0] - rect.centerx, target[1] - rect.centery
    distance = math.sqrt(dx**2 + dy**2)

    if distance > head_offset:  # Only move if outside the offset radius
        step_x = speed * (dx / distance)
        step_y = speed * (dy / distance)
        rect.centerx += int(step_x)
        rect.centery += int(step_y)
        return False  # Not yet at the target
    else:
        return True  # Close enough to stop moving


def find_closest_seaweed(turtle_rect, seaweed_list):
    """
    Find the closest seaweed to the turtle.
    """
    closest_seaweed = None
    min_distance = float('inf')

    for seaweed in seaweed_list:
        dx = seaweed.x - turtle_rect.centerx
        dy = seaweed.y - turtle_rect.centery
        distance = math.sqrt(dx**2 + dy**2)

        if distance < min_distance:
            closest_seaweed = seaweed
            min_distance = distance

    return closest_seaweed


def draw_score(screen, score_obj):
    """
    Draw the current score on the screen.
    """
    font = pygame.font.SysFont("Arial", 24)
    score_text = font.render(f"Score: {score_obj.get_score()}", True, (0, 0, 0))  # Black text
    screen.blit(score_text, (10, 10))  # Position at the top-left corner
# Load Eating Animation Frames
eating_frames = []
for i in range(0, 4):  # Assuming files are named eat_turtle0.png to eat_turtle3.png
    frame = pygame.image.load(f"assets/eat_turtle{i}.png").convert_alpha()
    frame.set_colorkey(colorkey)
    scaled_width = frame.get_width() * 4  # Scale the frame (4x size)
    scaled_height = frame.get_height() * 4
    scaled_frame = pygame.transform.scale(frame, (scaled_width, scaled_height))
    eating_frames.append(scaled_frame)

# Additional Variables for Eating Animation
eating = False  # Is the turtle eating?
eating_frame = 0  # Current frame in eating animation
eating_timer = 0  # Timer for eating animation
eating_delay = 150  # Delay between eating frames (in milliseconds)

def main():
    global current_frame, frame_timer, facing_left, score, sleeping, idle_time, state, turtle_rect
    global eat_timer, eating, eating_frame, eating_timer, eating_frames, walking_frames

    while True:
        dt = clock.tick(60)  # Get the time passed since the last frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Place seaweed where the user clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left-click
                    x, y = event.pos
                    seaweed_list.append(Seaweed(x, y))  # Add seaweed to list
                    sleeping = False  # Wake the turtle
                    idle_time = 0  # Reset idle time

        # Handle animation frame updates
        frame_timer += dt
        if frame_timer >= frame_delay:
            if state == "sleeping":
                current_frame = (current_frame + 1) % len(sleeping_frames)
            elif state == "walking":
                current_frame = (current_frame + 1) % len(walking_frames)
            elif state == "idle":
                current_frame = (current_frame + 1) % len(idle_frames)
            frame_timer = 0

        # Eating Animation Logic
        if eating:
            eating_timer += dt
            if eating_timer >= eating_delay:
                eating_timer = 0
                eating_frame += 1
                if eating_frame >= len(eating_frames):  # Animation complete
                    eating = False
                    eating_frame = 0  # Reset to first eating frame
                    state = "idle"  # Return to idle state
                    if eating_seaweed:  # Remove the seaweed after animation
                        seaweed_list.remove(eating_seaweed)
                        eating_seaweed = None
                        score.increase()
            state = "eating"

        # Determine turtle state and handle movement
        if not eating:  # Only handle other states if not eating
            if sleeping:
                state = "sleeping"
                idle_time = 0
            elif eat_timer > 0:  # Turtle is eating (delay before animation starts)
                eat_timer -= dt
                state = "idle"  # Show idle state during eating delay
            else:
                if seaweed_list:
                    closest_seaweed = find_closest_seaweed(turtle_rect, seaweed_list)
                    target_pos = (closest_seaweed.x, closest_seaweed.y)

                    # Check for direction flip
                    if target_pos[0] < turtle_rect.centerx and not facing_left:
                        facing_left = True
                        walking_frames = [pygame.transform.flip(frame, True, False) for frame in walking_frames]
                        eating_frames = [pygame.transform.flip(frame, True, False) for frame in eating_frames]
                    elif target_pos[0] > turtle_rect.centerx and facing_left:
                        facing_left = False
                        walking_frames = [pygame.transform.flip(frame, True, False) for frame in walking_frames]
                        eating_frames = [pygame.transform.flip(frame, True, False) for frame in eating_frames]

                    # Move turtle toward target
                    if move_toward_target(turtle_rect, target_pos, speed):
                        # If close enough, start eating
                        if closest_seaweed.check_eaten(turtle_rect):
                            eat_timer = eat_delay  # Start eating delay
                            eating = True  # Begin eating animation
                            eating_seaweed = closest_seaweed
                    state = "walking"
                else:
                    idle_time += dt
                    if idle_time >= idle_threshold:
                        state = "sleeping"
                    else:
                        state = "idle"

        # Clear screen and draw the current frame
        screen.fill((255, 223, 186))  # Beach sand yellow
        if state == "eating":
            screen.blit(eating_frames[eating_frame], turtle_rect)
        elif state == "sleeping":
            screen.blit(sleeping_frames[current_frame], turtle_rect)
        elif state == "walking":
            screen.blit(walking_frames[current_frame], turtle_rect)
        elif state == "idle":
            screen.blit(idle_frames[current_frame], turtle_rect)

        # Draw all seaweed
        for seaweed in seaweed_list:
            seaweed.draw(screen)

        # Draw the score
        draw_score(screen, score)

        # Update the display
        pygame.display.flip()


if __name__ == "__main__":
    main()
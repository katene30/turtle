import pygame
import sys
import random
import math
from seaweed import Seaweed  # Import the Seaweed class from seaweed.py

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

# Animation variables
current_frame = 0
frame_timer = 0
frame_delay = 150  # Delay between frames in milliseconds

# Position and movement variables
turtle_rect = idle_frames[0].get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
facing_left = False  # Tracks if the turtle is facing left
speed = 2  # Pixels per frame

# Seaweed list to store seaweed instances
seaweed_list = []

# Score variable
score = 0  # Initialize score

# Clock for controlling the game loop
clock = pygame.time.Clock()

# Define turtle states
sleeping = False
idle_time = 0  # Time the turtle has been idle (in milliseconds)
idle_threshold = 6000  # 1 minute of inactivity


def move_toward_target(rect, target, speed):
    """
    Move the turtle rect toward the target position at the given speed.
    """
    dx, dy = target[0] - rect.centerx, target[1] - rect.centery
    distance = math.sqrt(dx**2 + dy**2)

    if distance > speed:  # Avoid overshooting
        rect.centerx += int(speed * (dx / distance))
        rect.centery += int(speed * (dy / distance))
    else:  # If close to target, snap to it
        rect.center = target
    return rect


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


def draw_score(screen, score):
    """
    Draw the current score on the screen.
    """
    font = pygame.font.SysFont("Arial", 24)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))  # Black text
    screen.blit(score_text, (10, 10))  # Position at the top-left corner


def main():
    global current_frame, frame_timer, facing_left, score, sleeping, idle_time, idle_frames, turtle_rect

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


        # Handle frame timing for animation
        frame_timer += dt
        if frame_timer >= frame_delay:
            if sleeping:
                current_frame = (current_frame + 1) % len(sleeping_frames)  # Loop through sleeping frames
            else:
                current_frame = (current_frame + 1) % len(idle_frames)  # Loop through idle frames
            frame_timer = 0

        # If sleeping, skip movement logic
        if sleeping:
            idle_time = 0  # Reset idle time while sleeping
        else:
            if seaweed_list:
                closest_seaweed = find_closest_seaweed(turtle_rect, seaweed_list)
                target_pos = (closest_seaweed.x, closest_seaweed.y)

                # Check for direction flip
                if target_pos[0] < turtle_rect.centerx and not facing_left:
                    facing_left = True
                    idle_frames = [pygame.transform.flip(frame, True, False) for frame in idle_frames]
                elif target_pos[0] > turtle_rect.centerx and facing_left:
                    facing_left = False
                    idle_frames = [pygame.transform.flip(frame, True, False) for frame in idle_frames]

                # Move turtle toward target
                turtle_rect = move_toward_target(turtle_rect, target_pos, speed)

                # Check for collision (eating the seaweed)
                if closest_seaweed.check_eaten(turtle_rect):
                    seaweed_list.remove(closest_seaweed)  # Remove the eaten seaweed
                    score += 1  # Increase score by 1 when seaweed is eaten

                idle_time = 0  # Reset idle time if the turtle moves
            else:
                idle_time += dt  # Increment idle time if no seaweed is present

            # Put the turtle to sleep after 1 minute of inactivity
            if idle_time >= idle_threshold:
                sleeping = True
                current_frame = 0  # Reset animation frame

        # Clear screen with a beach-like yellow background
        screen.fill((255, 223, 186))  # Beach sand yellow

        # Draw the current frame based on the current animation (idle or sleeping)
        if sleeping:
            screen.blit(sleeping_frames[current_frame], turtle_rect)
        else:
            screen.blit(idle_frames[current_frame], turtle_rect)

        # Draw all seaweed in the list
        for seaweed in seaweed_list:
            seaweed.draw(screen)

        # Draw the score
        draw_score(screen, score)

        # Update display
        pygame.display.flip()


# Run the game loop
if __name__ == "__main__":
    main()

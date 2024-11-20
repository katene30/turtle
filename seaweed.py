# seaweed.py

import pygame

class Seaweed:
    def __init__(self, x, y):
        # Initialize the seaweed with a position and an image
        self.x = x
        self.y = y
        self.image = pygame.image.load("assets/seaweed.png").convert_alpha()  # Make sure you have a seaweed image
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 3, self.image.get_height() * 3))  # Scale by 2x

        self.rect = self.image.get_rect(center=(self.x, self.y))
    
    def draw(self, screen):
        # Draw the seaweed on the screen
        screen.blit(self.image, self.rect)
    
    def check_eaten(self, turtle_rect):
        """
        Check if the turtle has eaten the seaweed (collision detection).
        Returns True if the turtle collides with the seaweed.
        """
        return self.rect.colliderect(turtle_rect)

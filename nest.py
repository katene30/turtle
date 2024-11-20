import pygame
class Nest:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("assets/nest.png")  # Example image
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 4, self.image.get_height() * 4))  # Scale by 2x
        self.rect = self.image.get_rect(center=(x, y))

    def check_turtle_collision(self, turtle_rect):
        # Check if turtle is colliding with the nest
        return self.rect.colliderect(turtle_rect)

    def get_center(self):
        return self.rect.center

    def draw(self, screen):
        screen.blit(self.image, self.rect)

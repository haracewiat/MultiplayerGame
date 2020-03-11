import pygame

class Food:
    width = height = 10


    def __init__(self, startx, starty, color=(84, 165, 236)):
        self.x = startx
        self.y = starty
        self.color = color


    def draw(self, g):
        pygame.draw.rect(g, self.color, (self.x, self.y), self.width)
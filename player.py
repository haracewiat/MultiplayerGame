import pygame


class Player():
    width = height = 50

    def __init__(self, startx, starty, color=(84, 165, 236)):
        self.x = startx
        self.y = starty
        self.velocity = 4
        self.color = color

    def draw(self, g):
        pygame.draw.circle(g, self.color, (self.x, self.y), self.width)

    def move(self, key):
        if key == 0:
            self.x += self.velocity
        elif key == 1:
            self.x -= self.velocity
        elif key == 2:
            self.y -= self.velocity
        else:
            self.y += self.velocity

    def print(self):
        print(self.y)

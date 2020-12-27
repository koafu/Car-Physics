import pygame
from pygame import Vector2

class Wall:

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def show(self, screen):
        pygame.draw.line(screen, (0,0,0), self.start, self.end, 2)
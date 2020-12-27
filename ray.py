import pygame
from pygame import Vector2
from math import degrees, atan2

def scale(m, rMin, rMax, tMin, tMax):
    return ((m - rMin) / (rMax - rMin)) * (tMax - tMin) + tMin

class Ray:

    def __init__(self, pos, angle, length):
        self.pos = pos
        self.angle = angle
        self.dir = pos.rotate(self.angle)

        self.length = length # length of the ray
        self.detect = False # bool for when a obstacle is detected

    def update(self, direction):
        # if vel.magnitude() == 0:
        #     return

        self.dir = direction.rotate(self.angle).normalize()

    def cast(self, walls, pos, screen):
        walls_detected = 0
        min_dist = self.length + 1
        min_pt = None

        for wall in walls:
            x1 = wall.start.x
            y1 = wall.start.y
            x2 = wall.end.x
            y2 = wall.end.y
            x3 = self.pos.x
            y3 = self.pos.y
            x4 = self.pos.x + self.dir.x * self.length
            y4 = self.pos.y + self.dir.y * self.length

            denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if denominator == 0:
                continue

            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
            u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator

            if t > 0 and t < 1 and u > 0 and u < 1:
                pt = Vector2(x1 + t * (x2 - x1), y1 + t * (y2 - y1)) # intersection point
                # pygame.draw.circle(screen, (255, 0, 0), (int(pt.x), int(pt.y)), 3)
                self.detect = True
                walls_detected += 1
                dist = pos.distance_to(pt)
                if dist < min_dist:
                    min_dist = dist
                    min_pt = pt

        if walls_detected == 0:
            self.detect = False
            return 0 
        else:
            if min_pt:
                pygame.draw.circle(screen, (255, 0, 0), (int(min_pt.x), int(min_pt.y)), 3)

            # print(type(pos.distance_to(min_pt)))
            return scale(min_dist, 0, self.length, 1, 0)

    def show(self, screen):
        if self.detect:
            pygame.draw.line(screen, (255,0,0), self.pos,
                    (self.pos.x + self.dir.x * self.length,
                    self.pos.y + self.dir.y * self.length), 2)
        else:
            pygame.draw.line(screen, (140,160,185), self.pos,
                    (self.pos.x + self.dir.x * self.length,
                    self.pos.y + self.dir.y * self.length), 2)
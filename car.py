import pygame
from pygame import Vector2
from math import cos, sin, tan, radians, degrees, sqrt
from ray import Ray

class Car:

    def __init__(self, x, y):
        self.pos = Vector2(x, y)
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)

        self.angle = 0
        self.dir = Vector2(cos(radians(self.angle)), sin(-radians(self.angle)))

        self.turning_angle = 3
        self.max_speed = 8
        self.max_acc = 0.1
        self.max_braking = 0.08
        self.friction = 0.01

        self.dead = False

        self.r = 100
        self.forward_r = 250
        self.rays = []

        for angle in range(-15, 30, 15):
            self.rays.append(Ray(self.pos, angle, self.forward_r))
        for angle in range(90, -120, -30):
            if angle > 15 or angle < -15:
                self.rays.append(Ray(self.pos, angle, self.r))

        self.img_size = 30, 15
        self.img = pygame.image.load("assets/car.png").convert()
        self.img = pygame.transform.scale(self.img, self.img_size)
        self.img.set_colorkey((0,0,0))
        self.dead_img = pygame.image.load("assets/dead.png").convert()
        self.dead_img = pygame.transform.scale(self.dead_img, self.img_size)
        self.dead_img.set_colorkey((0,0,0))

        #for collision
        self.length = sqrt((self.img_size[0] / 2) ** 2 + (self.img_size[1] / 2) ** 2)
        self.length_angle = degrees(tan((self.img_size[1] / 2) / (self.img_size[0] / 2)))

    def update(self, walls, screen):
        self.vel += self.acc
        self.limit_speed()
        self.pos += self.vel
        self.acc *= 0

        self.collision(walls)

        for ray in self.rays:
            ray.cast(walls, self.pos, screen)
            ray.update(self.dir)

    def limit_speed(self):
        if self.vel.magnitude() > self.max_speed:
            self.vel.scale_to_length(self.max_speed)
        elif self.vel.magnitude() != 0 and self.vel.normalize() == -self.dir:
            self.vel *= 0

    def accelerate(self):
        self.acc = self.dir * self.max_acc

    def brake(self):
        self.acc = -(self.vel * self.max_braking)

    def cruise(self):
        self.acc = -(self.vel * self.friction)

    def turn_left(self):
        self.angle += self.turning_angle
        self.dir = Vector2(cos(radians(self.angle)), sin(-radians(self.angle)))
        self.vel = self.dir * self.vel.magnitude()

    def turn_right(self):
        self.angle -= self.turning_angle
        self.dir = Vector2(cos(radians(self.angle)), sin(-radians(self.angle)))
        self.vel = self.dir * self.vel.magnitude()

    def collision(self, walls):
        topright = Vector2(self.dir.rotate(self.length_angle) * self.length) + self.pos
        topleft = Vector2(self.dir.rotate(-self.length_angle) * self.length) + self.pos
        bottomright = Vector2(self.dir.rotate(self.length_angle + (180 - 2*self.length_angle)) * self.length) + self.pos
        bottomleft = Vector2(self.dir.rotate(-self.length_angle - (180 - 2*self.length_angle)) * self.length) + self.pos

        top_side = (topleft, topright)
        bottom_side = (bottomleft, bottomright)
        right_side = (topright, bottomright)
        left_side = (topleft, bottomleft)

        sides = [top_side, bottom_side, right_side, left_side]

        walls_detected = 0
        for side in sides:
            for wall in walls:
                x1 = wall.start.x
                y1 = wall.start.y
                x2 = wall.end.x
                y2 = wall.end.y
                x3 = side[0].x
                y3 = side[0].y
                x4 = side[1].x
                y4 = side[1].y

                denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
                if denominator == 0:
                    continue

                t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
                u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator

                if t > 0 and t < 1 and u > 0 and u < 1:
                    self.dead = True
                    walls_detected += 1
                    return

        if walls_detected == 0:
            self.dead = False

    def show(self, screen):
        for ray in self.rays:
            ray.show(screen)

        if self.dead:
            img_copy = pygame.transform.rotate(self.dead_img, self.angle)
        else:
            img_copy = pygame.transform.rotate(self.img, self.angle)
        screen.blit(img_copy, (int(self.pos.x - img_copy.get_width() / 2),
            int(self.pos.y - img_copy.get_height() / 2)))

        # pygame.draw.circle(screen, (0, 255, 0), (int(topright.x), int(topright.y)), 2)
        # pygame.draw.circle(screen, (0, 255, 0), (int(topleft.x), int(topleft.y)), 2)
        # pygame.draw.circle(screen, (0, 255, 0), (int(bottomright.x), int(bottomright.y)), 2)
        # pygame.draw.circle(screen, (0, 255, 0), (int(bottomleft.x), int(bottomleft.y)), 2)
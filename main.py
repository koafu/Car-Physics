import pygame, pickle
from pygame import Vector2
from car import Car
from wall import Wall

WIDTH = 1280
HEIGHT = 720

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Car Physics")
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.exit = False
        self.background = 40,40,40

        self.track = []
        self.start = None
        self.checkpoints = []
        self.load_track()

    def load_track(self):
        outer = open("track_maker/outer.pkl", "rb")
        outer_line = pickle.load(outer)
        outer.close()
        inner = open("track_maker/inner.pkl", "rb")
        inner_line = pickle.load(inner)
        inner.close()

        checkpoints_file = open("track_maker/checkpoints.pkl", "rb")
        self.checkpoints = pickle.load(checkpoints_file)
        self.start = Vector2(self.checkpoints[0])
        checkpoints_file.close()

        for i in range(len(outer_line)):
            if i == 0:
                continue
            elif i == len(outer_line) - 1:
                self.track.append(Wall(Vector2(outer_line[i]), Vector2(outer_line[0])))
            self.track.append(Wall(Vector2(outer_line[i-1]), Vector2(outer_line[i])))

        for i in range(len(inner_line)):
            if i == 0:
                continue
            elif i == len(inner_line) - 1:
                self.track.append(Wall(Vector2(inner_line[i]), Vector2(inner_line[0])))
            self.track.append(Wall(Vector2(inner_line[i-1]), Vector2(inner_line[i])))


    def run(self):

        car = Car(400, 400)

        while not self.exit:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            self.screen.fill(self.background)

            for wall in self.track:
                wall.show(self.screen)

            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                car.accelerate()
            elif keys[pygame.K_DOWN]:
                car.brake()
            else:
                car.cruise()

            if keys[pygame.K_LEFT]:
                car.turn_left()
            elif keys[pygame.K_RIGHT]:
                car.turn_right()

            car.update(self.track, self.screen)
            car.show(self.screen)

            self.clock.tick(self.fps)
            pygame.display.flip()

        pygame.quit()

if __name__ == '__main__':
    app = Main()
    app.run()
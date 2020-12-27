import pygame
import pickle
import os

class TrackMaker:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("TrackMaker")
        self.width = 1280
        self.height = 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False

        if os.path.exists("outer.pkl"):
            os.remove("outer.pkl")
        else:
            print("The file outer.pkl does not exist")

        if os.path.exists("inner.pkl"):
            os.remove("inner.pkl")
        else:
            print("The file inner.pkl does not exist")

        if os.path.exists("start.pkl"):
            os.remove("start.pkl")
        else:
            print("The file start.pkl does not exist")

        if os.path.exists("checkpoints.pkl"):
            os.remove("checkpoints.pkl")
        else:
            print("The file checkpoints.pkl does not exist")

        self.outer_file = open("outer.pkl", "wb")
        self.inner_file = open("inner.pkl", "wb")
        self.start_file = open("start.pkl", "wb")
        self.checkpoints_file = open("checkpoints.pkl", "wb")
        self.outer_line = []
        self.inner_line = []
        self.checkpoints = []
        self.start_pos = []

    def draw_track(self):

        for i in range(len(self.outer_line)):
            if i == 0:
                continue
            pygame.draw.line(self.screen, (0,0,0), self.outer_line[i-1], self.outer_line[i], 2)

        for i in range(len(self.inner_line)):
            if i == 0:
                continue
            pygame.draw.line(self.screen, (0,0,0), self.inner_line[i-1], self.inner_line[i], 2)


    def run(self):

        outer = False
        inner = False
        cp = False
        start = False

        while not self.exit:

            self.screen.fill((255,255,255))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print(self.outer_line)
                    self.exit = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if not outer:
                            outer = True
                        elif not inner:
                            inner = True
                        elif not start:
                            start = True
                        elif not cp:
                            cp = True

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not outer:
                        self.outer_line.append(event.pos)
                    elif not inner:
                        self.inner_line.append(event.pos)
                    elif not start:
                        self.start_pos = event.pos
                    elif not cp:
                        self.checkpoints.append(event.pos)

            if outer and inner and start and cp:
                pickle.dump(self.outer_line, self.outer_file)
                self.outer_file.close()

                pickle.dump(self.inner_line, self.inner_file)
                self.inner_file.close()

                pickle.dump(self.start_pos, self.start_file)

                pickle.dump(self.checkpoints, self.checkpoints_file)
                self.checkpoints_file.close()

                break

            self.draw_track()

            pygame.display.flip()
            self.clock.tick(self.ticks)

        pygame.quit()

if __name__ == '__main__':
    main = TrackMaker()
    main.run()
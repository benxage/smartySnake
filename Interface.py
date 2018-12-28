import GameLogic
import pygame
import sys

RED = pygame.Color(255, 0, 0)       # gameover
GREEN = pygame.Color(0, 255, 0)     # snake
BLACK = pygame.Color(0, 0, 0)       # score
WHITE = pygame.Color(255, 255, 255)  # background
BROWN = pygame.Color(165, 42, 42)   # food


class Interface:
    def __init__(self, width=72, height=46, display=False, player=None):
        self.game = GameLogic.Game(width, height)
        self.fpsController = pygame.time.Clock()
        self.display = display
        self.player = player  # AI function

    def showScore(self, playSurface):
        sFont = pygame.font.SysFont('monaco', 24)
        Ssurf = sFont.render('Score : {0}'.format(self.game.score), True, RED)
        Srect = Ssurf.get_rect()
        Srect.midtop = (80, 10)
        playSurface.blit(Ssurf, Srect)

    def getInputKey(self):
        key = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == ord('w'):
                    key = GameLogic.Direction.UP
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    key = GameLogic.Direction.DOWN
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    key = GameLogic.Direction.LEFT
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    key = GameLogic.Direction.RIGHT
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                    sys.exit()
        return key

    def playWithDisplay(self):
        # TODO spawn process to handle key
        while not self.game.gameOver():
            key = self.player(self.game.getState()
                              ) if self.player else self.getInputKey()
            self.game.update(key)

            playSurface = pygame.display.set_mode(
                (self.game.width * 10, self.game.height * 10))
            playSurface.fill(BLACK)
            for pos in self.game.body:
                pygame.draw.rect(playSurface, WHITE, pygame.Rect(
                    pos[0]*10, pos[1]*10, 9, 9))  # draw snake
            pygame.draw.rect(playSurface, GREEN, pygame.Rect(
                self.game.foodPos[0]*10, self.game.foodPos[1] * 10, 9, 9))  # draw food

            self.showScore(playSurface)
            pygame.display.flip()
            self.fpsController.tick(self.game.tick)

        pygame.quit()  # game over

    def playWithoutDisplay(self):
        while not self.game.gameOver():
            key = self.player(self.game.getState()
                              ) if self.player else self.getInputKey()
            self.game.update(key)

    def start(self):
        if self.display:
            check_errors = pygame.init()
            if check_errors[1] > 0:
                print("(!) Had {0} initializing errors with pygame, exiting...".format(
                    check_errors[1]))
                sys.exit(-1)

            print("(+) Snake Game successfully initialized with PyGame!")
            self.playWithDisplay()

        else:
            print("(+) Snake Game successfully initialized!")
            self.playWithoutDisplay()

        return self.game.score

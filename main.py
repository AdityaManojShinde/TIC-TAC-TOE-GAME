import pygame as game
import sys
import time
from pygame.locals import *

# CONSTANTS
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
SCREEN_BACKGROUND_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
CAPTION = "TIC TAC TOE"
FPS = 30

class TicTacToe:
    def __init__(self):
        game.init()
        self.screen = game.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + 100), 0, 32)
        game.display.set_caption(CAPTION)
        self.clock = game.time.Clock()

        # Game variables
        self.XO = 'x'
        self.winner = None
        self.draw = False
        self.board = [[None]*3 for _ in range(3)]

        # Load and scale images
        self.logo_img = game.transform.scale(game.image.load("./assets/logo.png"), (SCREEN_WIDTH, SCREEN_HEIGHT + 100))
        self.x_img = game.transform.scale(game.image.load("./assets/x.png"), (80, 80))
        self.o_img = game.transform.scale(game.image.load("./assets/o.png"), (80, 80))

    def draw_lines(self):
        # Draw vertical and horizontal lines
        for i in range(1, 3):
            game.draw.line(self.screen, LINE_COLOR, (SCREEN_WIDTH / 3 * i, 0), (SCREEN_WIDTH / 3 * i, SCREEN_HEIGHT), 7)
            game.draw.line(self.screen, LINE_COLOR, (0, SCREEN_HEIGHT / 3 * i), (SCREEN_WIDTH, SCREEN_HEIGHT / 3 * i), 7)

    def draw_status(self):
        message = ""

        if self.winner is None:
            message = self.XO.upper() + "'s Turn"
        else:
            message = self.winner.upper() + " won!"

        if self.draw:
            message = "Game Draw!"

        font = game.font.Font(None, 30)
        text = font.render(message, True, (255, 255, 255))

        self.screen.fill((0, 0, 0), (0, 400, 500, 100))
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, 450))
        self.screen.blit(text, text_rect)
        game.display.update()

    def game_window_init(self):
        self.screen.blit(self.logo_img, (0, 0))
        game.display.update()
        time.sleep(1)
        self.screen.fill(SCREEN_BACKGROUND_COLOR)
        self.draw_lines()
        self.draw_status()

    def check_win(self):
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] and self.board[row][0] is not None:
                self.winner = self.board[row][0]
                game.draw.line(self.screen, (250, 0, 0), (0, (row + 0.5) * SCREEN_HEIGHT / 3), (SCREEN_WIDTH, (row + 0.5) * SCREEN_HEIGHT / 3), 4)

        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] is not None:
                self.winner = self.board[0][col]
                game.draw.line(self.screen, (250, 0, 0), ((col + 0.5) * SCREEN_WIDTH / 3, 0), ((col + 0.5) * SCREEN_WIDTH / 3, SCREEN_HEIGHT), 4)

        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] is not None:
            self.winner = self.board[0][0]
            game.draw.line(self.screen, (250, 0, 0), (50, 50), (350, 350), 4)

        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] is not None:
            self.winner = self.board[0][2]
            game.draw.line(self.screen, (250, 0, 0), (350, 50), (50, 350), 4)

        if all(all(row) for row in self.board) and self.winner is None:
            self.draw = True

        self.draw_status()

    def draw_xo(self, row, col):
        posx = (row - 1) * SCREEN_WIDTH / 3 + 30
        posy = (col - 1) * SCREEN_HEIGHT / 3 + 30

        self.board[row-1][col-1] = self.XO

        if self.XO == 'x':
            self.screen.blit(self.x_img, (posy, posx))
            self.XO = 'o'
        else:
            self.screen.blit(self.o_img, (posy, posx))
            self.XO = 'x'

        game.display.update()

    def user_click(self):
        x, y = game.mouse.get_pos()

        row = (y // (SCREEN_HEIGHT / 3)) + 1
        col = (x // (SCREEN_WIDTH / 3)) + 1

        if self.board[int(row)-1][int(col)-1] is None:
            self.draw_xo(int(row), int(col))
            self.check_win()

    def reset_game(self):
        time.sleep(2)
        self.XO = 'x'
        self.draw = False
        self.winner = None
        self.board = [[None]*3 for _ in range(3)]
        self.game_window_init()

    def run(self):
        self.game_window_init()

        while True:
            for event in game.event.get():
                if event.type == QUIT:
                    game.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    self.user_click()
                    if self.winner or self.draw:
                        self.reset_game()

            game.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    TicTacToe().run()

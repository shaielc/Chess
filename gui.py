import pygame
from view.board import BoardView
from view.game import GameView
from controller.board import BoardController
from controller.game import GameController
from models.player import PlayerType
from models.board import Board
from view.history import HistoryView
from view.promotion import PromotionView
from threading import Thread
from time import sleep

def run_board(board: GameController):
    while True:
        board.handle_next()
        sleep(0.1)

pygame.font.init()

BG_COLOR = (128,128,128)
def init_board(width, height, screen):
    board_size = min(width,height)
    board_view = BoardView(board_size, board_size)
    promotion_view = PromotionView(board_size, 0, width-board_size, board_size//8, BG_COLOR)
    history_view = HistoryView(board_size, board_size//8, width-board_size, height - board_size//4, BG_COLOR)
    board_model = Board.default_board()
    game_view = GameView(board_view, promotion_view, history_view)
    return GameController(BoardController(board_model), players= {True: PlayerType.AI, False: PlayerType.AI}), game_view

def init_gui(width, height):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    screen.fill(BG_COLOR)
    clock = pygame.time.Clock()
    board, ui = init_board(width, height, screen)
    pygame.display.update()
    return screen, clock, board, ui

def update(screen, clock : pygame.time.Clock, game: GameController, ui: GameView):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.MOUSEBUTTONUP:
            event = ui.handle_click(click_pos=pygame.mouse.get_pos())
            game.add_event(event)
    
    ui.update(screen, game)
    clock.tick(10)
    pygame.display.update()
    return True


def run_gui(width,height):
    screen,clock,game,ui = init_gui(width, height)
    t = Thread(target=run_board, args=(game,))
    t.start()
    while True:
        if not update(screen,clock,game,ui):
            break
    pygame.quit()

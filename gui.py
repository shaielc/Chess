import pygame
from view.board import BoardView
from view.game import GameView
from controller.board import BoardController
from controller.game import GameController
from models.board import Board
from view.histoty import HistoryView
from view.promotion import PromotionView

pygame.font.init()

BG_COLOR = (128,128,128)
def init_board(width, height, screen):
    board_size = min(width,height)
    board_view = BoardView(board_size, board_size)
    promotion_view = PromotionView(board_size, 0, width-board_size, board_size//8, BG_COLOR)
    history_view = HistoryView(board_size, board_size//8, width-board_size, height - board_size//4, BG_COLOR)
    board_model = Board.default_board()
    game_view = GameView(board_view, promotion_view, history_view)
    return GameController(BoardController(board_model), game_view)

def init_gui(width, height):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    screen.fill(BG_COLOR)
    clock = pygame.time.Clock()
    board = init_board(width, height, screen)
    pygame.display.update()
    return screen, clock, board

def update(screen, clock , game: GameController):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.MOUSEBUTTONUP:
            game.handle_click()
    
    game.update_view(screen)
    clock.tick()
    pygame.display.update()
    return True


def run_gui(width,height):
    objs = init_gui(width, height)
    while True:
        if not update(*objs):
            break
    pygame.quit()

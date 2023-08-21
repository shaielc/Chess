import pygame
from controller.board import BoardController
from view.game import GameView
from time_func import timeit


class GameController:
    def __init__(self, board: BoardController, view: GameView) -> None:
        self.board = board
        self.view = view
        self.white = True
    
    @timeit
    def handle_click(self, click_pos):
        pos = self.view.screen_to_board(click_pos)
        if pos is not None:
            turn = self.board.handle_location_event(pos, self.white)
            if turn:
                self.white = not self.white
            return
        piece = self.view.screen_to_promotion(click_pos)
        if piece is not None:
            self.board.promote(piece)

    def update_view(self, screen):
        self.view.update(screen, self.board)
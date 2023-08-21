import pygame
from controller.board import BoardController
from models.events import Event, EventType
from time_func import timeit
from enum import Enum

class Player(Enum):
    HUMAN=0
    AI=1


class GameController:
    def __init__(self, board: BoardController, players: dict[bool, Player]) -> None:
        self.board = board
        self.white = True
        self.players = players
    
    @timeit
    def handle_event(self, event: Event):
        if self.players[self.white].value != event.source.value:
            return
        if event.event_type == EventType.BOARD:
            pos = event.payload
            turn = self.board.handle_location_event(pos, self.white)
            if turn:
                self.white = not self.white
            return
        if event.event_type == EventType.PROMOTION:
            piece = event.payload
            self.board.promote(piece)
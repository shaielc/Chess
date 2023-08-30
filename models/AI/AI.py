from models.board import Board
from models.events import Event, EventSourceType, EventType
from models.pieces.piece import PiecesContainer
from models.player import PlayerType
from abc import ABC, abstractmethod
from time_func import timeit

class AI(ABC):
    TYPE=PlayerType.AI

    def __init__(self, white=True) -> None:
        super().__init__()
        self.calculating = False
        self.started = False
        self.event = None
        self.white = white
    
    def get_event(self,) -> Event:
        return self.event
    
    def set_turn(self, ):
        self.started = False
        self.event = None
        self.calculating = False

    def is_done(self,) -> bool:
        return self.started and not self.calculating

    def move(self, target):
        self.event = Event(EventType.MOVE, EventSourceType.AI, target)
    
    def promotion(self, piece):
        self.event = Event(EventType.PROMOTION, EventSourceType.AI, piece)

    def get_possible_moves(self, board: Board):
        relevant_pieces = board.pieces.filter_by_player(self.white)
        possible_moves = {}
        for p in relevant_pieces:
            piece_moves = board.get_valid_moves(p)
            if len(piece_moves) > 0:
                possible_moves[p] = piece_moves
        return possible_moves
    
    def get_pressure(self, board):
        relevant_pieces = board.pieces.filter_by_player(self.white)
        threats = {}
        for p in relevant_pieces:
            _threats = p.threatning(board.pieces)
            if len(_threats):
                threats[p] = _threats
        return threats
    
    def get_threats(self, board: Board):
        relevant_pieces = board.pieces.filter_by_player(not self.white)
        threats = {}
        for p in relevant_pieces:
            _threats = p.threatning(board.pieces)
            if len(_threats):
                threats[p] = _threats
        return threats


    @abstractmethod
    def calc_move(self, board: Board):
        pass

    def handle_calc_event(self, board: Board):
        self.calculating = True
        self.started = True
        done = self.calc_move(board)
        self.calculating = not done
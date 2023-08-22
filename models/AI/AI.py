from models.board import Board
from models.events import Event, EventSourceType, EventType
from models.pieces.piece import PiecesContainer
from models.player import PlayerType
from abc import ABC, abstractmethod

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

    @abstractmethod
    def calc_move(self, board: Board):
        pass

    def handle_calc_event(self, board: Board):
        self.calculating = True
        self.started = True
        self.calc_move(board)
        self.calculating = False
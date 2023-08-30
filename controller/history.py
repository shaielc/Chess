from models.board import Board
from models.events import Event, EventType
from models.history import History, Move

class HistoryController:
    def __init__(self, board: Board) -> None:
        self.board = board
        self.history = History([])
        self.index = -1
    
    def prev(self, ):
        move: Move = self.board.moves.pop()
        self.history.add_move(move)
        move.revert(self.board.pieces)

    def next(self,):
        if len(self.history) == 0:
            return
        move: Move = self.history.pop()
        self.board.moves.add_move(move)
        move.apply(self.board.pieces)
    
    def resume(self,):
        while len(self.history):
            self.next()
    
    def handle_event(self, event: Event):
        if event.event_type == EventType.NEXT:
            self.next()
        if event.event_type == EventType.PREV:
            self.prev()
        return False
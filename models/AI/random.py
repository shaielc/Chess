from models.AI.AI import AI
from models.board import Board
from models.events import Event, EventSourceType, EventType
from models.pieces.queen import Queen
import random

class RandomAI(AI):
    """definitly not an AI - returns random moves, always promotes to queen.
    """
    def calc_move(self, board: Board):
        if board.need_to_promote is not None:
            p = board.need_to_promote
            self.promotion(Queen(p.x,p.y,p.white))
            return True
        moves = None
        move = None
        piece = None
        while piece is None:
            piece = random.sample(tuple(board.pieces.filter_by_player(self.white)),1)[0]
            moves = tuple(board.get_valid_moves(piece))
            if len(moves) == 0:
                piece = None
        move = random.sample(moves,1)[0]
        self.move((piece,move))
        return True
        
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
        
        possible_moves = self.get_possible_moves(board)
        piece, moves = random.sample(possible_moves.items(),1)[0]
        move = random.sample(moves,1)[0]
        self.move((piece,move))
        return True
        
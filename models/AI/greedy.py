from collections import defaultdict
from models.AI.AI import AI
from models.board import Board
from models.pieces.king import King
from models.pieces.queen import Queen
from models.pieces.piece import Piece, PieceTypes, PiecesContainer
import random


def cmp(x,y):
    for a,b in zip(x,y):
        if a < b:
            return -1
        if a > b:
            return 1
        if a == b:
            continue
    return 0

class Threats:
    def __init__(self, threats: dict[Piece, set]) -> None:
        self.threats = defaultdict(int)
        super().__init__()
        for moves in threats.values():
            self += moves
    
    def __iadd__(self, moves: set):
        for move in moves:
            self.threats[move] += 1
        return self
    
    def __isub__(self, moves: set):
        for move in moves:
            self.threats[move] -= 1
        return self
    
    def __contains__(self, other):
        return other in self.threats  and self.threats[other] > 0

class GreedyAI(AI):
    """Greedy AI - evaluates best current move, without considering future moves
    """
    def calc_move(self, board: Board):
        if board.need_to_promote is not None:
            p = board.need_to_promote
            self.promotion(Queen(p.x,p.y,p.white))
            return True
        
        threats = set()
        for t in self.get_threats(board).values():
            threats.update(t)
        possible_moves: dict[Piece, set] = self.get_possible_moves(board)
        pressure_points = Threats(self.get_pressure(board))
        kings = {k.white: k for k in board.pieces.filter_by_type(PieceTypes.KING)}
        chosen = None
        chosen_rank = None
        for piece, moves in possible_moves.items():
            for move in moves:
                rank = self.rank(piece, move, threats, board.pieces.locations.get(move), kings, board.pieces, pressure_points)
                comparison = cmp(rank, chosen_rank) if chosen_rank is not None else 1
                if comparison == 1:
                    chosen_rank = rank
                    chosen = (piece, move)
        print(self.white, chosen_rank[-1])
        self.move(chosen)
        return True

    def position_score(self, x, y, type: PieceTypes):
        if type == PieceTypes.PAWN:
            score = 2*(3.5 - abs(x - 4)) + (y if not self.white else 6-y)
            return score
        elif type == PieceTypes.KING:
            return (3.5 - abs(x - 3.5)) - (7 - y if self.white else y)/2
        else:
            direction = 1 - 2*self.white
            return (3.5 - abs(x - (3 if self.white else 4))) + (3.5 - abs(y - (3 if self.white else 4)))
    
    @staticmethod
    def king_freedom(king, threats, pieces: PiecesContainer):
        king_freedom = 9
        for i in range(-1,2):
            if not (0 <= king.x +i <= 7):
                king_freedom -= 3
                continue
            for j in range(-1,2):
                if not (0 <= king.y +j <= 7):
                    king_freedom -= 1
                    continue
                position = (king.x+i, king.y+j)
                occupier = pieces.locations.get(position)
                if occupier is not None and occupier != king and occupier.white == king.white:
                    king_freedom -= 1
                    continue
                king_freedom -= position in threats
        return king_freedom

    def rank(self, piece: Piece, move: tuple[int,int], threats, target: Piece, kings: dict[bool, King], pieces, pressure_points):
        new_threats = piece.threats_in_position(*move, piece.white, pieces, piece)
        if piece.TYPE == PieceTypes.PAWN and piece.can_promote(move[1]):
            new_threats = Queen.threats_in_position(*move, piece.white, pieces, piece)
        current_threats = piece.threatning(pieces)
        
        target_score = 0
        if target is not None:
            target_score = target.TYPE.value +1
        if target_score < piece.TYPE.value + 1 and move in threats:
            target_score = 0
        piece_score = piece.TYPE.value+1 if piece.TYPE != PieceTypes.KING else -500
        move_score = self.position_score(move[0], move[1], piece.TYPE)**2
        move_threatened = 0
        if move in threats:
            move_threatened = -piece.TYPE.value
        position_score = self.position_score(piece.x, piece.y, piece.TYPE)**2
        position_threatened = 0
        if (piece.x, piece.y) in threats:
            position_threatened = piece.TYPE.value
        other_king = kings[not self.white]
        can_check = (other_king.x, other_king.y) in new_threats
        current_king_freedom = self.king_freedom(other_king, pressure_points, pieces)
        pressure_points -= current_threats
        pressure_points += new_threats
        new_king_freedom = self.king_freedom(other_king, pressure_points, pieces)
        pressure_points -= new_threats
        pressure_points += current_threats
        return ( 
            new_king_freedom != 1,
            target_score,
            position_threatened, 
            move_threatened, 
            can_check * (current_king_freedom - new_king_freedom ), 
            move_score - position_score,  
            (current_king_freedom - new_king_freedom ), 
            move_score, 
            piece_score, 
            new_king_freedom
        )

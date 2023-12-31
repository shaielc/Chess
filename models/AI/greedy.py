from collections import defaultdict
from models.AI.AI import AI
from models.board import Board
from models.pieces.king import King
from models.pieces.queen import Queen
from models.pieces.piece import Piece, PieceTypes, PiecesContainer, is_defending
import random

def cmp(x,y):
    for a,b in zip(x,y):
        if a < b:
            return -1
        if a > b:
            return 1
        if a == b:
            continue
    if len(x) > len(y):
        return 1
    if len(x) < len(y):
        return -1
    return 0

class Threats:
    def __init__(self, threats: dict[Piece, set]) -> None:
        self.threats = defaultdict(set)
        super().__init__()
        self += threats

    def __iadd__(self, threats: dict[Piece, set]):
        for piece, moves in threats.items():
            for move in moves:
                self.threats[move].add(piece)
        return self
    
    def __isub__(self, threats: dict[Piece, set]):
        for piece, moves in threats.items():
            for move in moves:
                self.threats[move].remove(piece)
        return self
    
    def __contains__(self, other):
        return other in self.threats  and len(self.threats[other]) > 0
    
    def __getitem__(self, move):
        return self.threats[move]

class GreedyAI(AI):
    """Greedy AI - evaluates best current move, without considering future moves
    """
    def calc_move(self, board: Board):
        if board.need_to_promote is not None:
            p = board.need_to_promote
            self.promotion(Queen(p.x,p.y,p.white))
            return True
        
        threats = Threats(self.get_threats(board))
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
        # print(self.white, chosen_rank[-1])
        if chosen is None:
            return False
        self.move(chosen)
        return True

    def position_score(self, x, y, type: PieceTypes):
        if type == PieceTypes.PAWN:
            score = 2*(3.5 - abs(x - 4)) + (y if not self.white else 6-y)
            return score
        elif type == PieceTypes.KING:
            return (3.5 - abs(x - 3.5)) - (7 - y if self.white else y)/2
        else:
            return (3.5 - abs(x - 3.5)) + (3.5 - abs(y - 3.5))*2
    
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

    @staticmethod
    def calc_trade(piece, target, threatning_score, pressure_score):
        total_score = 0
        last_value = piece.TYPE.value
        if target is not None:
            total_score += target.TYPE.value
        for threat, pressure in zip(threatning_score, pressure_score):
            total_score -= last_value
            if total_score > 0:
                break
            total_score += threat
            last_value = pressure
        if len(threatning_score) > len(pressure_score):
            total_score -= last_value
        return total_score

    @staticmethod
    def get_threatened_score(piece, move, target, threats, pressure_points):
        if move not in threats:
            return 0
        if target is None and move not in pressure_points:
            return -piece.TYPE.value
        

        threatning_pieces = threats[move]
        pressuring_pieces = pressure_points[move]
        threatning_score = sorted({p.TYPE.value for p in threatning_pieces})
        pressure_score = sorted({p.TYPE.value for p in pressuring_pieces})
        
        # if move in pressure_points and len(threatning_pieces) == 1 and list(threatning_pieces)[0].TYPE == PieceTypes.KING:
        #     return 0
        
        trade_score = GreedyAI.calc_trade(piece, target, threatning_score, pressure_score)
        if trade_score < 0:
            return -piece.TYPE.value
        return 0
    

    def rank(self, piece: Piece, move: tuple[int,int], threats, target: Piece, kings: dict[bool, King], pieces: PiecesContainer, pressure_points):
        new_threats = piece.threats_in_position(*move, piece.white, pieces, piece)
        if piece.TYPE == PieceTypes.PAWN and piece.can_promote(move[1]):
            new_threats = Queen.threats_in_position(*move, piece.white, pieces, piece)
        current_threats = piece.threatning(pieces)
        other_king = kings[not self.white]
        current_king_freedom = self.king_freedom(other_king, pressure_points, pieces)
        
        target_score = 0
        if target is not None:
            target_score = target.TYPE.value

        piece_score = piece.TYPE.value+1 if piece.TYPE != PieceTypes.KING else -500
        move_score = self.position_score(move[0], move[1], piece.TYPE)**2

        threatened_pieces = (p for p in (pieces.locations.get(pos) for pos in current_threats) if p is not None)
        defense_score = -sum(p.TYPE.value for p in threatened_pieces if p.white == self.white)
        attack_score = -sum(p.TYPE.value for p in threatened_pieces if p.white != self.white)
        
        pressure_points -= {piece: current_threats}
        move_threatened = self.get_threatened_score(piece, move, target, threats, pressure_points)
        if move_threatened != 0:
            target_score = 0
        
        position_score = self.position_score(piece.x, piece.y, piece.TYPE)**2
        position_threatened = -self.get_threatened_score(piece, (piece.x, piece.y), None, threats, pressure_points)
        position = (piece.x, piece.y)
        if position in threats:
            defending = is_defending(piece, pieces)
            for defends, attacker in defending.items():
                if defends.TYPE.value > piece.TYPE.value:
                    position_threatened = 0
        
        can_check = (other_king.x, other_king.y) in new_threats
        
        pressure_points += {piece: new_threats}
        new_king_freedom = self.king_freedom(other_king, pressure_points, pieces)
        pressure_points -= {piece: new_threats}
        pressure_points += {piece: current_threats}
        return (
            position_threatened + target_score,
            move_threatened, 
            target_score,
            can_check * (current_king_freedom - new_king_freedom ), 
            defense_score,
            attack_score,
            move_score - position_score,  
            (current_king_freedom -new_king_freedom ), 
            move_score, 
            piece_score, 
            new_king_freedom
        )

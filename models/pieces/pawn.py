from models.pieces.piece import Piece, PieceTypes, PiecesContainer
from models.pieces.util import position_status,PositionStatus

class Pawn(Piece):
    TYPE = PieceTypes.PAWN
    def __init__(self, x, y, white=True) -> None:
        self.en_passant = False
        self.can_eat = {}
        super().__init__(x, y, white)

    def valid_moves(self, pieces: PiecesContainer) -> list:
        
        direction =(1-2*self.white)
        basic_move = (self.x, self.y+direction)
        double_move = (self.x, self.y+2*direction)
        moves = set()
        can_move_doulbe = self.y == (6 if self.white else 1)
        self.can_eat = {}
        
        status, _ = position_status(self, basic_move, pieces)
        if status == PositionStatus.EMPTY:
            moves.add(basic_move)
        
        if can_move_doulbe:
            status, _ = position_status(self, double_move, pieces)
            if status == PositionStatus.EMPTY:
                moves.add(double_move)
        
        moves.update(self.threatning(pieces, exclude_empty=True))
        return moves

    def threatning(self, pieces: PiecesContainer, exclude_empty=False) -> list:
        direction = (1-2*self.white)
        possible_moves = {(self.x+1, self.y+ direction), (self.x-1, self.y+ direction)}
        moves = set()
        for m in possible_moves:
            status, piece = position_status(self, m, pieces)
            if status == PositionStatus.ENEMY:
                moves.add(m)
                self.can_eat[m] = piece
            if status == PositionStatus.EMPTY and not exclude_empty:
                moves.add(m)
        
        moves.update(self.check_en_passant(pieces))
        
        return moves
    
    def check_en_passant(self, pieces: PiecesContainer):
        direction = (1-2*self.white)
        moves = set()
        if self.y != (3 if self.white else 4):
            return moves
        
        p = pieces.locations.get((self.x+1, self.y))
        if p is not None and p.TYPE == PieceTypes.PAWN and p.en_passant:
            moves.add((self.x+1, self.y + direction))
            self.can_eat[(self.x+1, self.y + direction)] = p

        p = pieces.locations.get((self.x-1, self.y))
        if p is not None and p.TYPE == PieceTypes.PAWN and p.en_passant:
            moves.add((self.x-1, self.y + direction))
            self.can_eat[(self.x-1, self.y + direction)] = p

        return moves

    def can_promote(self,):
        return self.y == (0 if self.white else 7)

    def apply_en_passant(self, target):
        p = self.can_eat.get(target)
        if p is None:
            return False
        if p.TYPE != PieceTypes.PAWN:
            return False
        if not p.en_passant:
            return False
        p.en_passant = False
        if self.TYPE != PieceTypes.PAWN:
            return False
        if target[0] != p.x:
            return False
        if target[1] != (p.y + (2*p.white - 1)):
            return False
        return True
    
    def move(self, x, y):
        if abs(y - self.y) == 2:
            self.en_passant = True
        return super().move(x, y)
        
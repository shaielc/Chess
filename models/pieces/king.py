from models.pieces.piece import PieceTypes, Piece, STRAIGHT_VECS, DIAG_VECS, PiecesContainer
from models.pieces.rook import Rook
from models.pieces.util import directions, find_threats, status_check_position, status_check_threatning

class King(Piece):
    TYPE = PieceTypes.KING
    def __init__(self, x, y, white=True) -> None:
        super().__init__(x, y, white)
        self.moved =False
        self.castle = {}
        self.checked = False

    def _get_moves(self, pieces, check_type=None):
        return directions(self, STRAIGHT_VECS + DIAG_VECS, pieces, single=True, status_state=check_type)
    
    def valid_moves(self, pieces: PiecesContainer) -> list:
        moves = self._get_moves(pieces, status_check_position)
        return moves
    
    def threatning(self, pieces: list) -> list:
        moves = self._get_moves(pieces, status_check_threatning)
        return moves
    
    def move(self, x, y):
        self.moved = True
        return super().move(x, y)
    
    def can_castle(self, pieces: list[Piece]):
        self.castle = {}

        if self.moved:
            return []
        if len(find_threats(self.x, self.y,pieces, self.white)) > 0:
            return []
        
        rooks = [p for p in pieces if p.TYPE == PieceTypes.ROOK and p.white == self.white]
        castles = []
                
        for r in rooks:
            if r.isin(0,self.y) and not r.moved:
                move = self.x - 2, self.y
                if len(find_threats(*move,pieces, white=self.white)) > 0:
                    continue
                if len(find_threats(move[0]+1,move[1],pieces, white=self.white)) > 0:
                    continue
                if (move[0]+1,move[1]) not in r.valid_moves(pieces):
                    continue
                self.castle[move] = (r, self.x - 1)
                castles.append(move)
            if r.isin(7, self.y) and not r.moved:
                move = self.x + 2, self.y
                if len(find_threats(*move,pieces, white=self.white)) > 0:
                    continue
                if len(find_threats(move[0]-1,move[1],pieces, white=self.white)) > 0:
                    continue
                if (move[0]-1,move[1]) not in r.valid_moves(pieces):
                    continue
                self.castle[move] =  (r, self.x + 1)
                castles.append(move)
        return castles

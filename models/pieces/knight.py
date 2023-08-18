from models.pieces.piece import PieceTypes, Piece, KNIGHT_MOVES
from models.pieces.util import directions

class Knight(Piece):
    TYPE = PieceTypes.KNIGHT
    def valid_moves(self, pieces: list) -> list:
        return  directions(self, KNIGHT_MOVES, pieces, single=True)
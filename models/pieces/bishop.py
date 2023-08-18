from models.pieces.piece import Piece,PieceTypes,DIAG_VECS
from models.pieces.util import directions

class Bishop(Piece):
    TYPE = PieceTypes.BISHOP
    def valid_moves(self, pieces: list) -> list:
        return directions(self, DIAG_VECS, pieces)
from models.pieces.piece import Piece,PieceTypes, DIAG_VECS, STRAIGHT_VECS
from models.pieces.util import directions


class Queen(Piece):
    TYPE = PieceTypes.QUEEN
    def valid_moves(self, pieces):
        return directions(self, STRAIGHT_VECS + DIAG_VECS, pieces)
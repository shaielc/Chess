from models.pieces.piece import Piece,PieceTypes, DIAG_VECS, STRAIGHT_VECS, PiecesContainer
from models.pieces.util import directions


class Queen(Piece):
    TYPE = PieceTypes.QUEEN
    def _get_moves(self, pieces: PiecesContainer, check_type: dict) -> list:
        return directions(self, STRAIGHT_VECS + DIAG_VECS, pieces, status_state=check_type)
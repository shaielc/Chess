from models.pieces.piece import Piece,PieceTypes,DIAG_VECS,PiecesContainer
from models.pieces.util import directions

class Bishop(Piece):
    TYPE = PieceTypes.BISHOP
    def _get_moves(self, pieces: PiecesContainer, check_type: dict) -> list:
        return directions(self, DIAG_VECS, pieces, status_state=check_type)
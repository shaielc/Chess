from models.pieces.piece import PieceTypes, Piece, KNIGHT_MOVES, PiecesContainer
from models.pieces.util import directions

class Knight(Piece):
    TYPE = PieceTypes.KNIGHT
    def _get_moves(self, pieces: PiecesContainer, check_type: dict) -> list:
        return  directions(self, KNIGHT_MOVES, pieces, single=True, status_state=check_type)
        
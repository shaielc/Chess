from models.pieces.piece import Piece, PieceTypes,STRAIGHT_VECS, PiecesContainer
from models.pieces.util import directions

class Rook(Piece):
    TYPE = PieceTypes.ROOK
    def __init__(self, x, y, white=True) -> None:
        self.moved = False
        super().__init__(x, y, white)

    def _get_moves(self, pieces: PiecesContainer, check_type: dict) -> list:
        return directions(self, STRAIGHT_VECS, pieces, status_state=check_type)
    
    def move(self, x, y):
        self.moved = True
        return super().move(x, y)
       
    
    

                        

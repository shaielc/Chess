from models.pieces.piece import Piece, PieceTypes,STRAIGHT_VECS
from models.pieces.util import directions

class Rook(Piece):
    TYPE = PieceTypes.ROOK
    def valid_moves(self, pieces: list[Piece]) -> list:
        return directions(self, STRAIGHT_VECS, pieces)
       
    
    

                        

import pygame
from models.pieces.piece import Piece, PieceTypes

class PieceView:
    IMAGE_PATTERN = "resources/%(type)s%(color)st60.png"
    def __init__(self, img) -> None:
        self.img = img
    
    @classmethod
    def resolve_image(cls, piece: Piece):
        color = 'l' if piece.white else 'd'
        if piece.TYPE == PieceTypes.PAWN:
            piece_type = "p"
        elif piece.TYPE == PieceTypes.ROOK:
            piece_type = "r"
        elif piece.TYPE == PieceTypes.BISHOP:
            piece_type = "b"
        elif piece.TYPE == PieceTypes.QUEEN:
            piece_type = "q"
        elif piece.TYPE == PieceTypes.KING:
            piece_type = "k"
        elif piece.TYPE == PieceTypes.KNIGHT:
            piece_type = "n"
        else:
            raise ValueError("Got invalid peice type %s" % piece.TYPE)
        
        return cls.IMAGE_PATTERN % {"color": color, "type": piece_type}

    def move(self, screen, x, y):
        screen.blit(self.img, (x,y))
    
    @classmethod
    def from_piece(cls, piece, width, height=None):
        return PieceView(pygame.transform.scale(
                pygame.image.load(PieceView.resolve_image(piece)),
                (width, width) if height is None else (width, height)
            ))



from dataclasses import dataclass
from typing import Union
from models.pieces.piece import Piece, PieceTypes, PiecesContainer
from models.pieces.rook import Rook

piece_abbreviations = {
    PieceTypes.PAWN: 'P',
    PieceTypes.KNIGHT: 'N',
    PieceTypes.BISHOP: 'B',
    PieceTypes.ROOK: 'R',
    PieceTypes.QUEEN: 'Q',
    PieceTypes.KING: 'K'
}

def convert_pos_to_notation( x, y):
    return chr(ord('a') + x) + str(y)

@dataclass
class Move:
    piece: Piece
    start: tuple
    end: tuple

    def __str__(self) -> str:
        text = piece_abbreviations[self.piece.TYPE]
        text += convert_pos_to_notation(*self.end)
        return text
    
    def apply(self, pieces: PiecesContainer):
        pieces.move(self.piece, *self.end)
    
    def revert(self, pieces: PiecesContainer):
        pieces.move(self.piece, *self.start)

@dataclass
class Take(Move):
    taken: Piece

    def apply(self, pieces: PiecesContainer):
        pieces.remove(self.taken)
        return super().apply(pieces)

    def revert(self, pieces: PiecesContainer):
        pieces.add(self.taken)
        return super().revert(pieces)

@dataclass
class Promotion:
    piece: Piece
    promote: Piece

    def apply(self, pieces: PiecesContainer):
        pieces.remove(self.piece)
        pieces.add(self.promote)
    
    def revert(self, pieces: PiecesContainer):
        pieces.add(self.piece)
        pieces.remove(self.promote)

@dataclass
class Castle(Move):
    rook_move: Move

    def apply(self, pieces: PiecesContainer):
        self.rook_move.apply(pieces)
        return super().apply(pieces)
    
    def revert(self, pieces: PiecesContainer):
        self.rook_move.revert(pieces)
        return super().apply(pieces)

class History:
    def __init__(self, moves: list[Move]) -> None:
        self.moves = moves

    def add_move(self, move: Move):
        self.moves.append(move)

    def __len__(self,):
        return len(self.moves)
    
    def __getitem__(self, index):
        return self.moves[index]
    
    def pop(self,):
        return self.moves.pop()
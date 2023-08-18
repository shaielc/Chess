from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from time_func import timeit

class PiecesContainer:
    def __init__(self, piece_list) -> None:
        self.pieces: list[Piece] = piece_list
        self.locations = {(p.x, p.y): p for p in piece_list}
        self.removed_pieces = set()

    def remove(self, piece):
        self.pieces.remove(piece)
        p = self.locations[piece.x, piece.y]
        if p == piece:
            self.locations[piece.x, piece.y] = None
        self.removed_pieces.add(piece)
    
    def add(self, piece):
        self.pieces.append(piece)
        self.locations[piece.x, piece.y] = piece
        
        if piece in self.removed_pieces:
            self.removed_pieces.remove(piece)

    def move(self, piece: Piece, x,y):
        self.locations[piece.x, piece.y] = None
        self.locations[x,y] = piece
        piece.move(x,y)

    def filter_by_type(self, piece_type) -> PiecesContainer:
        return PiecesContainer([p for p in self.pieces if piece_type == p.TYPE])
    
    def filter_by_player(self, white=True) -> PiecesContainer:
        return PiecesContainer([p for p in self.pieces if white == p.white])
    
    def __iter__(self, ) -> list[Piece]:
        return iter(self.pieces)


STRAIGHT_VECS = [(0,1), (1,0), (-1,0), (0,-1)]
DIAG_VECS = [(1,1), (-1,1), (-1,-1), (1,-1)]
KNIGHT_MOVES = [(2,1), (2,-1), (-2,1), (-2,-1), (-1,2), (1,2), (-1,-2), (1,-2)]

class PieceTypes(Enum):
    PAWN = 0
    BISHOP = 1
    KNIGHT=2
    ROOK=4
    QUEEN=8
    KING=16


class Piece(ABC):
    TYPE=None
    def __init__(self, x, y, white=True) -> None:
        self.x = x
        self.y = y
        self.white = white
    
    @abstractmethod
    def valid_moves(self, pieces: list) -> list:
        raise NotImplemented("Using abstract class Piece")
    
    def threatning(self, pieces: list) -> list:
        return self.valid_moves(pieces)
    
    def __repr__(self) -> str:
        return "<%s (%s,%d)>" % (self.TYPE, chr(ord('A') + self.x), self.y)
    
    def isin(self, x, y):
        return self.x == x and self.y == y
    
    def same_color(self, other):
        return self.white == other.white
    
    def move(self, x, y):
        self.x = x
        self.y = y

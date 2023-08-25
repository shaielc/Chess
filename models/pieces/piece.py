from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from models.pieces.util import status_check_position, status_check_threatning

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

    def filter_piece(self, piece):
        return PiecesContainer([p for p in self.pieces if p != piece])
    
    def __iter__(self, ) -> list[Piece]:
        return iter(self.pieces)
    
    def __len__(self,):
        return len(self.pieces)

STRAIGHT_VECS = [(0,1), (1,0), (-1,0), (0,-1)]
DIAG_VECS = [(1,1), (-1,1), (-1,-1), (1,-1)]
KNIGHT_MOVES = [(2,1), (2,-1), (-2,1), (-2,-1), (-1,2), (1,2), (-1,-2), (1,-2)]

class PieceTypes(Enum):
    PAWN = 1
    BISHOP = 2
    KNIGHT=4
    ROOK=8
    QUEEN=16
    KING=32


class Piece(ABC):
    TYPE=None
    def __init__(self, x, y, white=True) -> None:
        self.x = x
        self.y = y
        self.white = white

    
    def valid_moves(self, pieces: PiecesContainer) -> set:
        moves = self._get_moves(pieces, check_type=status_check_position)
        return moves
    
    def threatning(self, pieces: list) -> set:
        moves = self._get_moves(pieces, check_type=status_check_threatning)
        return moves
    
    @abstractmethod
    def _get_moves(self, pieces: PiecesContainer, check_type: dict) -> set:
        raise NotImplemented("Using abstract class Piece")
    
    def __repr__(self) -> str:
        return "<%s (%s,%d)>" % (self.TYPE, chr(ord('A') + self.x), self.y)
    
    def isin(self, x, y):
        return self.x == x and self.y == y
    
    def same_color(self, other):
        return self.white == other.white
    
    @classmethod
    def threats_in_position(cls, x, y, white, pieces: PiecesContainer, ignore: Piece):
        return cls(x,y, white).threatning(pieces.filter_piece(ignore))
    
    def move(self, x, y):
        self.x = x
        self.y = y

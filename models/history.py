from dataclasses import dataclass

from models.pieces.piece import Piece, PieceTypes

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
    taken: Piece | None

    def __str__(self) -> str:
        text = piece_abbreviations[self.piece.TYPE]
        text += "" if self.taken is None else "x"
        text += convert_pos_to_notation(*self.end)
        return text

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
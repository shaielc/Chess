from models.pieces.piece import PiecesContainer
from models.pieces.knight import Knight


def test_knight_moves():
    knight = Knight(4,4)
    moves = knight.valid_moves(PiecesContainer([]))
    assert(len(moves) == 8)
    assert(set(((2,3), (3,2), (5,6), (6,5), (6,3), (3,6), (2,5),(5,2))) == moves)

def test_occupied():
    knight = Knight(4,4)
    moves = knight.valid_moves(PiecesContainer([Knight(2,3), Knight(3,2,white=False)]))
    assert(len(moves) == 7)
    assert(set(((3,2), (5,6), (6,5), (6,3), (3,6), (2,5),(5,2))) == moves)

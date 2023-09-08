
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.pieces.piece import Piece, PiecesContainer
from enum import Enum
from time_func import timeit
import math

class PositionStatus(Enum):
    OFF=0
    EMPTY=1
    ALLY=2
    ENEMY=3

def position_status(source: Piece, pos, pieces: PiecesContainer):
    x,y = pos
    if not on_board(x,y):
        return PositionStatus.OFF, None

    piece = pieces.locations.get((x,y))
    if piece is None:
        return PositionStatus.EMPTY, None
    
    if piece.same_color(source):
        return PositionStatus.ALLY, piece
    else:
        return PositionStatus.ENEMY, piece


def get_status(source, pos, pieces):
    status, _ = position_status(source, pos, pieces)
    return status

status_check_position = {
    PositionStatus.OFF: (False, False),
    PositionStatus.ALLY: (False,False),
    PositionStatus.ENEMY: (True, False),
    PositionStatus.EMPTY: (True, True)
}

status_check_collision = {
    PositionStatus.OFF: (False, False),
    PositionStatus.ALLY: (True,False),
    PositionStatus.ENEMY: (True, False),
    PositionStatus.EMPTY: (False, True)
}

status_check_defending = {
    PositionStatus.OFF: (False, False),
    PositionStatus.ALLY: (True, False),
    PositionStatus.ENEMY: (False, False),
    PositionStatus.EMPTY: (False, True)
}

status_check_threatning = {
    PositionStatus.OFF: (False, False),
    PositionStatus.ALLY: (True,False),
    PositionStatus.ENEMY: (True, False),
    PositionStatus.EMPTY: (True, True)
}

def get_all_moves(query, pieces):
    return {p: p.threatning(pieces) for p in query}

def find_threats(x, y, pieces: PiecesContainer, white=None):
    test_pieces = pieces
    if white is not None:
        test_pieces = pieces.filter_by_player(not white)
    result = get_all_moves(test_pieces, pieces)
    return [other for other in result if (x,y) in result[other]]

def directions(piece: Piece, vectors, pieces: PiecesContainer, single=False, status_state=None):
    if status_state is None:
        status_state=status_check_position
    positions = [(piece.x, piece.y)] * len(vectors)
    directions = [ (pos, vec) for pos, vec in zip(positions, vectors)]
    moves = set()
    while len(directions):
        directions = [(add_vector(pos, vec), vec) for pos, vec  in directions]
        statuses = [ get_status(piece, pos, pieces) for pos, vec in  directions]
        checks = [status_state[status] for status in statuses]
        next_directions = []
        for ((pos, vec), (valid, next_valid)) in zip(directions, checks):
            if valid:
                moves.add(pos)
            if next_valid:
                next_directions.append((pos,vec))
        directions = next_directions
        if single:
            break
    
    return moves

def get_direction(a, b):
    vec = (b[0]- a[0], b[1] - a[1])
    gcd = math.gcd(*vec)
    return (vec[0]/gcd, vec[1]/gcd)

def add_vector(pos, vec):
    return pos[0] + vec[0], pos[1] + vec[1]

def on_board(x,y):
    if x < 0 or y < 0:
        return False
    if x > 7 or y > 7:
        return False
    return True



from models.pieces.piece import Piece, DIAG_VECS, STRAIGHT_VECS, KNIGHT_MOVES, PieceTypes, PiecesContainer
from enum import Enum
from time_func import timeit

def _check_position(source, pos, pieces: PiecesContainer):
    status: PositionStatus 
    status, _ = position_status(source, pos, pieces)

    if status == PositionStatus.OFF or status == PositionStatus.ALLY:
        return False, False
    if status == PositionStatus.ENEMY:
        return True, False
    if status == PositionStatus.EMPTY:
        return  True, True
    raise ValueError("Invalid status position %s" % status)

def _check_collision(source, pos, pieces):
    status: PositionStatus 
    status, _ = position_status(source, pos, pieces)

    if status == PositionStatus.OFF:
        return False, False
    if status == PositionStatus.ALLY:
        return True, False
    if status == PositionStatus.ENEMY:
        return True, False
    if status == PositionStatus.EMPTY:
        return  False, True
    raise ValueError("Invalid status position %s" % status)

def get_all_moves(query, pieces):
    return {p: p.threatning(pieces) for p in query}

def find_threats(x, y, pieces: PiecesContainer, white=None):
    test_pieces = pieces
    if white is not None:
        test_pieces = pieces.filter_by_player(not white)
    result = get_all_moves(test_pieces, pieces)
    return [other for other in result if (x,y) in result[other]]



def directions(piece: Piece, vectors, pieces: PiecesContainer, single=False, check_blocking=False):
    callback=_check_position
    if check_blocking:
        callback = _check_collision
    positions = [(piece.x, piece.y)] * len(vectors)
    directions = [ (pos, vec) for pos, vec in zip(positions, vectors)]
    moves = set()
    while len(directions):
        directions = [(add_vector(pos, vec), vec) for pos, vec  in directions]
        checks = [ callback(piece, pos, pieces) for pos, vec in  directions]
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

def add_vector(pos, vec):
    return pos[0] + vec[0], pos[1] + vec[1]

def on_board(x,y):
    if x < 0 or y < 0:
        return False
    if x > 7 or y > 7:
        return False
    return True

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

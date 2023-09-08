from models.AI.greedy import GreedyAI, Threats
from models.pieces.bishop import Bishop
from models.pieces.knight import Knight
from models.pieces.pawn import Pawn
from models.board import Board


def calc_trade(piece, target, board, ai):
    threats = Threats(ai.get_threats(board))
    pressure = Threats(ai.get_pressure(board))
    pressure -= {piece: piece.threatning(board.pieces)}
    threatning_score = sorted({p.TYPE.value for p in threats[(target.x,target.y)]})
    pressure_score = sorted({p.TYPE.value for p in pressure[(target.x,target.y)]})
    return ai.calc_trade(piece, target,threatning_score, pressure_score)


def test_pawn_trade():
    piece = Pawn(0,5)
    target = Pawn(1,4,white=False)
    board = Board([piece, Pawn(2,5),  target, Pawn(2,3,white=False)])
    ai = GreedyAI(True)
    trade_score = calc_trade(piece, target, board, ai)
    assert(trade_score == 1)

def test_trade_scenario_1():
    pawn = Pawn(0,2, white=False)
    bishop = Bishop(2,4)
    board = Board([pawn, bishop, Knight(1,0, white=False), Knight(2,1)])
    ai = GreedyAI(True)
    
    threats = Threats(ai.get_threats(board))
    pressure = Threats(ai.get_pressure(board))
    pressure -= {bishop: bishop.threatning(board.pieces)}
    trade_score = calc_trade(bishop, pawn, board, ai)    
    assert(trade_score == Pawn.TYPE.value + Knight.TYPE.value - Bishop.TYPE.value)

    move_threatened = ai.get_threatened_score(bishop, (pawn.x, pawn.y), pawn, threats, pressure)
    assert(move_threatened == 0)


def test_trade_scenario_2():
    pawn = Pawn(0,2, white=False)
    bishop = Bishop(2,4)
    board = Board([pawn, bishop, Knight(1,0, white=False)])
    ai = GreedyAI(True)

    trade_score = calc_trade(bishop, pawn, board, ai)
    
    assert(trade_score == -1)
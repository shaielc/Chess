from models.AI.greedy import GreedyAI, Threats
from models.pieces.pawn import Pawn
from models.board import Board

def test_pawn_trade():
    piece = Pawn(0,5)
    target = Pawn(1,4,white=False)
    board = Board([piece, Pawn(2,5),  target, Pawn(2,3,white=False)])
    ai = GreedyAI(True)
    threats = Threats(ai.get_threats(board))
    pressure = Threats(ai.get_pressure(board))
    threatning_score = sorted({p.TYPE.value for p in threats[(1,4)]})
    pressure_score = sorted({p.TYPE.value for p in pressure[(1,4)]})
    trade_score = ai.calc_trade(piece, target,threatning_score, pressure_score)
    assert(trade_score == 1)


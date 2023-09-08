
import time
from functools import wraps
from models.pieces.piece import PiecesContainer
from models.history import Castle, History, Move, Promotion, Take
from models.pieces.bishop import Bishop
from models.pieces.king import King
from models.pieces.knight import Knight
from models.pieces.pawn import Pawn
from models.pieces.piece import Piece, PieceTypes, DIAG_VECS, STRAIGHT_VECS, KNIGHT_MOVES
from models.pieces.queen import Queen
from models.pieces.rook import Rook
from models.pieces.util import directions, find_threats, position_status, PositionStatus, status_check_collision, get_direction


from time_func import timeit



class Board:
    def __init__(self, pieces=[]) -> None:
        self.pieces: PiecesContainer = PiecesContainer(pieces)
        self.need_to_promote = None
        self.is_checked = None
        self.moves = History([])
        self.finished = False
        checks = self.check_for_check()
        if len(checks) > 0:
            self.is_checked = checks[0]

    def promote(self, piece: Piece):
        if self.need_to_promote is None:
            return False
        x = self.need_to_promote.x
        y = self.need_to_promote.y
        piece.move(x,y)
        promotion = Promotion(self.need_to_promote, piece)
        promotion.apply(self.pieces)
        self.moves.add_move(promotion)
        self.need_to_promote = None
        
        checks = self.check_for_check()
        if len(checks) > 0:
            self.is_checked = checks[0]
        else:
            self.is_checked = None
        self.update_endgame(not piece.white)

    def check_for_check(self,):
        kings = self.pieces.filter_by_type(piece_type=PieceTypes.KING)
        threats = [(k, find_threats(k.x, k.y, self.pieces, k.white)) for k in kings]
        checked = []
        for k, threat in threats:
            k.checked = len(threat) > 0
            if len(threat) > 0:
                checked.append(k)
        return checked


    def _get_valid_check_move_other(self, king, possible_moves, threats):
        final_moves = set()
        
        if len(threats) > 1:
            return final_moves
                
        filt = directions(king, DIAG_VECS + STRAIGHT_VECS, self.pieces)
        filt.update(directions(king, KNIGHT_MOVES, self.pieces, True))
        filtered_moves = {m for m in possible_moves if m in filt}
        
        threat = threats[0]
        for m in filtered_moves:
            if threat.isin(*m):
                final_moves.add(m)
                continue
            if threat.TYPE == PieceTypes.KNIGHT:
                continue

            threat_vec = get_direction((king.x, king.y), (threat.x,threat.y))
            target_vec = get_direction((king.x, king.y), m)
            
            if threat_vec != target_vec:
                continue
            
            final_moves.add(m)
                
        return final_moves
    
    def _get_valid_moves_other(self, piece, king, possible_moves, threats):
        relevant_threats = []
        for threat in threats:
            if threat.TYPE == PieceTypes.KNIGHT:
                continue
            if threat.TYPE == PieceTypes.KING:
                continue
            if threat.TYPE == PieceTypes.PAWN:
                continue

            threat_vec = get_direction((king.x, king.y), (threat.x,threat.y))
            target_vec = get_direction((king.x, king.y), (piece.x, piece.y))
            if threat_vec != target_vec:
                continue
            threat_vec = get_direction((threat.x,threat.y),(king.x, king.y))
            hit = tuple(directions(piece, [threat_vec], self.pieces, status_state=status_check_collision))
            if len(hit) == 0:
                continue
            if self.pieces.locations[hit[0]] != king:
                continue
            relevant_threats.append(threat)
        
        if len(relevant_threats) == 0:
            return possible_moves
        
        final_moves = set()
        threat = relevant_threats[0]
        for m in possible_moves:
            if threat.isin(*m):
                final_moves.add(m)
                continue
            if threat.TYPE == PieceTypes.KNIGHT:
                continue

            threat_vec = get_direction((king.x, king.y), (threat.x,threat.y))
            target_vec = get_direction((king.x, king.y), m)
            
            if threat_vec != target_vec:
                continue

            final_moves.add(m)
        
        return final_moves
        
    def _get_valid_moves_king(self, king,  possible_moves):
        final_moves = set()
        for m in possible_moves:
            if len(find_threats(m[0], m[1], self.pieces, king.white)) == 0:
                final_moves.add(m)
        if king.checked == False:
            final_moves.update(king.can_castle(self.pieces)) # this is bad.
        else:
            threats = find_threats(king.x, king.y, self.pieces, king.white)
            for threat in threats:
                for m in tuple(final_moves):
                    if m == (threat.x, threat.y):
                        continue
                    threat_vec = get_direction((king.x, king.y), (threat.x,threat.y))
                    target_vec = get_direction(m, (threat.x,threat.y))
                    
                    if target_vec != threat_vec:
                        continue
                    final_moves.remove(m)
                    
        return final_moves

    def get_valid_moves(self, piece: Piece):
        if self.finished or self.need_to_promote is not None: # TODO: need to make sure any none "const" function updates state.
            return []
        
        possible_moves = piece.valid_moves(self.pieces)
        
        if piece.TYPE == PieceTypes.KING:
            return self._get_valid_moves_king(piece, possible_moves)
        if self.is_checked is not None:
            threats = find_threats(self.is_checked.x, self.is_checked.y, self.pieces, piece.white)
            possible_moves = self._get_valid_check_move_other( self.is_checked, possible_moves, threats)
        
        threats = find_threats(piece.x, piece.y , self.pieces, piece.white)
        kings = self.pieces.filter_by_type(PieceTypes.KING).filter_by_player(piece.white).pieces
        if len(kings) == 0:
            return possible_moves # NOTE: inidication of bad design
        return self._get_valid_moves_other(piece, kings[0], possible_moves, threats)

    
    def check_for_endgame(self, white):
        player_pieces = self.pieces.filter_by_player(white)
        if len(self.pieces) == 2:
            return True
        for p in player_pieces:
            if len(self.get_valid_moves(p)) > 0:
                return False
        return True
    
    def update_endgame(self, white):
        self.finished = self.check_for_endgame(white)
    
    def move(self, piece: Piece, target):
        if self.finished:
            return False
        
        if self.need_to_promote is not None:
            return False
        
        if target not in self.get_valid_moves(piece):
            return False
        
        status, target_piece = position_status(piece, target, self.pieces)
        
        if status == PositionStatus.OFF:
            return False
        
        if status == PositionStatus.ALLY:
            return False

        move = Move(piece, (piece.x, piece.y), target)
        if status == PositionStatus.ENEMY:
            move = Take(piece, (piece.x,piece.y), target, taken=target_piece)
        elif piece.TYPE == PieceTypes.PAWN:
            other = self.en_passant(piece, target)
            if other is not None:
                move = Take(piece, (piece.x,piece.y), target, taken=other)
        
        if piece.TYPE == PieceTypes.KING and target in piece.castle:
            rook, pos = piece.castle[target]
            move = Castle(piece, (piece.x,piece.y), target, Move(rook, (rook.x, rook.y), pos))
        
        if piece.TYPE == PieceTypes.PAWN and piece.can_promote(y=target[1]):
            self.need_to_promote = piece
        else:
            self.need_to_promote = None
            
        
        move.apply(self.pieces)
        self.moves.add_move(move)

        checks = self.check_for_check()
        if len(checks) == 0:
            self.is_checked = None
        else:
            if self.is_checked in checks:
                self.revert()
                return False
            if checks[0].white == piece.white:
                self.revert()
                return False
            self.is_checked = checks[0]
        
        if self.need_to_promote is None:
            self.update_endgame(not piece.white)
        
        self.disable_en_passant()

        return True
    
    def disable_en_passant(self,):
        if len(self.moves) < 2:
            return
        p = self.moves[-2].piece
        if p.TYPE != PieceTypes.PAWN:
            return
        p.en_passant = False #

    def _revert_en_passant(self, ):
        if len(self.moves) == 0:
            return
        m: Move = self.moves.pop()
        p = m.piece
        prev = m.start
        if p.TYPE != PieceTypes.PAWN:
            return
        if abs(p.y - prev[1]) == 2:
            p.en_passant =True

    def revert(self,):
        m:Move = self.moves.pop()
        m.revert(self.pieces)
        
    def en_passant(self, piece: Pawn, target):
        if piece.is_en_passant(target):
            return piece.can_eat[target]
        return 
    
    @classmethod
    def default_board(cls,):
        return cls(
            [ Pawn(i, 6, True) for i in range(8) ]  + 
            [ Pawn(i, 1, False) for i in range(8) ] +
            [ Rook(7,7,True),  Knight(6,7, True),  Bishop(5,7,True),  King(4,7, True),  Queen(3,7,True),  Bishop(2,7, True),  Knight(1,7,True),  Rook(0,7, True)] +
            [ Rook(7,0,False), Knight(6,0, False), Bishop(5,0,False), King(4,0, False), Queen(3,0,False), Bishop(2,0, False), Knight(1,0,False), Rook(0,0, False)]
        )
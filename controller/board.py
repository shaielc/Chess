from models.board import Board
from view.board import BoardView
from models.pieces.piece import Piece

class BoardController:
    def __init__(self, model: Board) -> None:
        self.model = model
        self.selected_piece = None

    def handle_location_event(self, pos, white=True):
        if self.model.finished:
            return
        if self.model.need_to_promote is not None:
            return
        x,y = pos
        
        if self.selected_piece is not None:
            result = self._move(self.selected_piece, x, y)
            if result is not None:
                self.selected_piece = None
                return result
                
        found = False
        for p in self.model.pieces:
            if p.x == x and p.y == y:
                if p.white == white:
                    self.selected_piece = p
                found=True
                break
        if not found:
            self.selected_piece = None
        
        return False
    
    def _move(self, piece, x, y):
        if self.model.move(piece, (x,y)):
            if self.model.need_to_promote is None:
                return True
            return False
    
    def handle_move_event(self, piece: Piece, pos, white=True):
        if piece.white != white:
            return
        result = self._move(piece, *pos)
        if result is not None:
            return result
        return False
    
    def get_history(self,):
        return self.model.moves.moves

    def get_eaten_pieces(self, ):
        return self.model.pieces.removed_pieces

    def get_pieces(self, ):
        return self.model.pieces
    
    def get_valid_moves(self, ):
        if self.model.need_to_promote is not None:
            return []
        if self.selected_piece is not None:
            return self.model.get_valid_moves(self.selected_piece)
        return []

    def promote(self, piece):
        if self.model.need_to_promote is None:
            return False
        self.model.promote(piece)
        return True

    def check_promotion(self,):
        return self.model.need_to_promote

    def is_finished(self,):
        return self.model.finished, self.model.is_checked.white if self.model.is_checked is not None else None 
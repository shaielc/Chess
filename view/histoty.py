from controller.board import BoardController
from models.pieces.piece import Piece
from view.piece import PieceView

class CapturedPieces:
    def __init__(self, x, y, width, height) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    
    def update(self, screen, pieces: list[Piece]):
        for i, p in enumerate(sorted(pieces, key=lambda p: p.TYPE.value)):
            pv = PieceView.from_piece( p, self.width//8, self.height//2)
            pv.move(screen, (i % 8)* self.width//8, self.y + i // 8 * self.height//2)

class HistoryView:
    def __init__(self, x, y, width, height, bg) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bg =bg
        self.white_captured = CapturedPieces(self.x, self.height - self.height//4, self.width, self.height//4)
        self.black_captured = CapturedPieces(self.x, 0,self.width, self.height//4)
    
    def update(self, screen, board: BoardController):
        subsurface = screen.subsurface((self.x, self.y, self.width, self.height))
        subsurface.fill(self.bg)

        eaten_pieces = board.get_eaten_pieces()
        self.black_captured.update(subsurface, [p for p in eaten_pieces if not p.white])
        self.white_captured.update(subsurface, [p for p in eaten_pieces if p.white])
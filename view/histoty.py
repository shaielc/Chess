from controller.board import BoardController
from models.pieces.piece import Piece
from view.piece import PieceView
import pygame

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

class NotationView:
    FONT = "Ariel"
    def __init__(self, x,y, width, height) -> None:
        self.font = pygame.font.SysFont(self.FONT, 30)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    

    def update(self, screen, history):
        pygame.draw.rect(screen, (25,25,25), (self.x,self.y, self.width, self.height))
        
        lines = 0
        text = "History: "
        for m in history:
            
            line_width = self.font.size(text)[0]
            move = str(m)
            if line_width + self.font.size(move)[0] > self.width:
                text_surf = self.font.render(text, False, (200, 200, 200))
                screen.blit(text_surf, (self.x, self.y + lines * self.font.get_height()))
                text = move
                lines +=1
            else:
                text += move + ","
        
        text_surf = self.font.render(text, False, (200, 200, 200))
        screen.blit(text_surf, (self.x, self.y + lines * self.font.get_height()))

class HistoryView:
    
    def __init__(self, x, y, width, height, bg) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bg =bg
        self.white_captured = CapturedPieces(0, self.height - self.height//4, self.width, self.height//4)
        self.black_captured = CapturedPieces(0, 0,self.width, self.height//4)
        self.notation_view = NotationView(0, self.height//4, self.width, self.height//2)
    
    def update(self, screen, board: BoardController):
        subsurface = screen.subsurface((self.x, self.y, self.width, self.height))
        subsurface.fill(self.bg)

        eaten_pieces = board.get_eaten_pieces()
        self.black_captured.update(subsurface, [p for p in eaten_pieces if not p.white])
        self.white_captured.update(subsurface, [p for p in eaten_pieces if p.white])
        self.notation_view.update(subsurface, board.get_history())
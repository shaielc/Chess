import pygame
from models.pieces.bishop import Bishop
from models.pieces.knight import Knight

from models.pieces.queen import Queen
from models.pieces.rook import Rook
from view.piece import PieceView

class PromotionView:
    def __init__(self, x, y, width, height, bg) -> None:
        self.x = x 
        self.y = 0
        self.width = width
        self.height = height
        self.bg = bg
        self.white = None
        self.whites = [(p,PieceView.from_piece(p, self.height)) for p in (Queen(8,8, white=True), Rook(8,8, white=True), Knight(8,8, white=True), Bishop(8,8, white=True))]
        self.blacks = [(p,PieceView.from_piece(p, self.height)) for p in (Queen(8,8, white=False), Rook(8,8, white=False), Knight(8,8, white=False), Bishop(8,8, white=False))]
    
    def update(self, screen, piece=None):
        if piece is None:
            self.white =None
            subsurface = screen.subsurface((self.x, self.y, self.width, self.height))
            subsurface.fill(self.bg)
            return
        self.white = piece.white
        self.y = (screen.get_height() - self.height) if self.white else 0
        subsurface = screen.subsurface((self.x, self.y, self.width, self.height))
        subsurface.fill(self.bg)

        target = self._get_current()
        
        for i,(_,pv) in enumerate(target):
            pv: PieceView
            pv.move(subsurface, self.height *i, 0)
        
    def _get_current(self, ):
        if self.white == True:
            return self.whites
        else:
            return self.blacks
    
    def __contains__(self, pos):
        x,y = pos
        if x < self.x:
            return False
        if x > self.x + self.width:
            return False
        if y < self.y:
            return False
        if y > self.y + self.height:
            return False
        return True
    
    def screen_to_game(self, pos):
        x,y = pos
        x = (x-self.x)//self.height
        if x > 3:
            return None
        return self._get_current()[x][0]
        
        
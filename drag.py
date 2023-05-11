import pygame

from const import *


class Drag:

    def __init__(self):
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_col = 0
        self.piece = None
        self.dragging = False

    def update_mouse(self, pos):
        self.mouseX, self.mouseY = pos  # (x,y)

    def save_initial_pos(self, pos):
        self.initial_row = pos[1] // SQSIZE
        self.initial_col = pos[0] // SQSIZE

    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True

    def undrag_piece(self):
        self.piece = None
        self.dragging = False

    def blit_icon(self, surface):
        img_center = self.mouseX, self.mouseY
        self.piece.texture_rect = self.piece.img.get_rect(center=img_center)
        surface.blit(self.piece.img, self.piece.texture_rect)





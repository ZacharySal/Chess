import pygame

from const import *
from board import Board
from drag import Drag


class Game:

    def __init__(self):
        self.board = Board()
        self.drag = Drag()
        self.themes = [
            [(240, 236, 184), (75, 115, 153, 255)],
            [(234, 235, 200), (119, 154, 88)],
            [(134, 35, 120), (19, 254, 190)],
            [(134, 35, 120), (19, 254, 190)]
        ]
        self.theme_option = 0

    def change_bg(self):
        self.theme_option += 1
        self.theme_option %= len(self.themes)

    def show_bg(self, surface):

        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = self.themes[self.theme_option][0]  # light squares
                else:
                    color = self.themes[self.theme_option][1] # dark squares

                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)

                pygame.draw.rect(surface, color, rect)

    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece

                    # make sure piece is not being dragged before blit
                    if piece is not self.drag.piece:
                        piece.img = pygame.image.load(piece.texture).convert_alpha()
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2  # center y first, then x
                        piece.texture_rect = piece.img.get_rect(center=img_center)
                        surface.blit(piece.img, piece.texture_rect)

    def show_legal_moves(self, surface):
        if self.drag.dragging:
            piece = self.drag.piece

            # show legal moves for each piece
            for move in piece.moves:
                # if not self.board.will_expose_king(piece, move):
                    square = self.board.squares[move.final.row][move.final.col]

                    # if square contains a rival piece
                    if square.has_rival_piece(piece.color):
                        color = (128, 128, 128)
                        center = move.final.col * SQSIZE + SQSIZE // 2, move.final.row * SQSIZE + SQSIZE // 2
                        rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                        pygame.draw.circle(surface, color, center, 40, width=10)

                    else:
                        color = (128, 128, 128)
                        center = move.final.col * SQSIZE + SQSIZE // 2, move.final.row * SQSIZE + SQSIZE // 2
                        rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                        pygame.draw.circle(surface, color, center, 13)

    def show_last_move(self, surface):
        if self.board.last_move is not None:

            initial_square = self.board.last_move.initial
            final_square = self.board.last_move.final

            for square in [initial_square, final_square]:
                if (square.row + square.col) % 2 == 0:
                    color = (88, 190, 254, 255)
                else:
                    color = (38, 140, 204, 255)
                rect = (square.col * SQSIZE, square.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    def show_invalid_move(self, surface):

        color = (255, 0, 0)
        row = self.drag.initial_row
        col = self.drag.initial_col

        rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
        pygame.draw.rect(surface, color, rect)


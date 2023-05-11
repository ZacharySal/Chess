import pygame
import sys

from const import *
from game import Game
from move import Move
from square import Square
from engine import Engine

from stockfish import Stockfish

# TODO:
# en passant optional
# allow user to set level of stockfish


class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game()
        self.engine = Engine()

    def mainloop(self):

        game = self.game
        screen = self.screen
        drag = self.game.drag
        board = self.game.board
        engine = self.engine

        while True:

            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_legal_moves(screen)
            game.show_pieces(screen)

            # if board.next_player == 'black':
               # pygame.time.delay(200)
               # engine.get_fen(board)
               # engine.create_engine_move(board)
               # board.next_turn()
               # game.show_bg(screen)
               # game.show_last_move(screen)
               # game.show_pieces(screen)

            if drag.dragging:
                drag.blit_icon(screen)

            for event in pygame.event.get():

                #  mouse click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    drag.update_mouse(event.pos)

                    clicked_row = drag.mouseY // SQSIZE
                    clicked_col = drag.mouseX // SQSIZE

                    # does clicked square contain a piece
                    if board.squares[clicked_row][clicked_col].has_piece():

                        clicked_piece = board.squares[clicked_row][clicked_col].piece

                        if board.next_player == clicked_piece.color:
                            drag.save_initial_pos(event.pos)
                            drag.drag_piece(clicked_piece)
                            board.calc_moves(clicked_piece, clicked_row, clicked_col, True)
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_legal_moves(screen)
                            game.show_pieces(screen)

                # mouse movement
                elif event.type == pygame.MOUSEMOTION:
                    if drag.dragging:
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_legal_moves(screen)
                        game.show_pieces(screen)
                        drag.update_mouse(event.pos)
                        drag.blit_icon(screen)

                # click released
                elif event.type == pygame.MOUSEBUTTONUP:

                    if drag.dragging:
                        drag.update_mouse(event.pos)

                        released_row = drag.mouseY // SQSIZE
                        released_col = drag.mouseX // SQSIZE

                        initial = Square(drag.initial_row, drag.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        if board.is_valid_move(drag.piece, move):
                            board.move(drag.piece, move)
                            # board.is_game_over()
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            board.next_turn()

                        drag.undrag_piece()

                # theme change
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        game.change_bg()

                # quit
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


main = Main()
main.mainloop()

from stockfish import Stockfish
from const import *
from square import Square
from move import Move

class Engine:

    def __init__(self):
        self.stockfish = Stockfish(path="stockfish/stockfish_15_win_x64_avx2/stockfish_15_x64_avx2")
        self.best_move = ""

        self.d = {
            'rook': 'r',
            'bishop': 'b',
            'knight': 'n',
            'queen': 'q',
            'king': 'k',
            'pawn': 'p',
        }

        self.row_dict = {
            8: 0,
            7: 1,
            6: 2,
            5: 3,
            4: 4,
            3: 5,
            2: 6,
            1: 7,
        }

        self.col_dict = {
            'a': 0,
            'b': 1,
            'c': 2,
            'd': 3,
            'e': 4,
            'f': 5,
            'g': 6,
            'h': 7,
        }

        self.fen = ""

    def get_fen(self, board):

        self.fen = ""

        for row in range(ROWS):
            empty_space = 0
            for col in range(COLS):
                if board.squares[row][col].has_piece():
                    piece = board.squares[row][col].piece
                    if empty_space != 0:
                        self.fen += f"{empty_space}"
                        name = self.d[piece.name].upper() if piece.color == "white" else self.d[piece.name]
                        self.fen += name
                        empty_space = 0
                    else:
                        name = self.d[piece.name].upper() if piece.color == "white" else self.d[piece.name]
                        self.fen += name

                else:
                    empty_space += 1
            if empty_space != 0:
                self.fen += str(empty_space)
            if row != 7:
                self.fen += "/"

        next = 'b' if board.next_player == 'black' else 'w'
        self.fen += f" {next}"

        castling_options = board.castling_options()
        self.fen += f' {castling_options}'
        self.fen += " -"
        self.fen += " 0"
        self.fen += " 1"

        # print(self.fen)
        # print(f'is fen valid? {self.stockfish.is_fen_valid(self.fen)}')

        self.stockfish.set_fen_position(f'{self.fen}')

    def create_engine_move(self, board):
        self.best_move = self.stockfish.get_best_move()
        print(self.best_move)

        initial_row = abs(int(self.best_move[1]) - 8)
        initial_col = self.col_dict[self.best_move[0]]

        final_row = abs(int(self.best_move[3]) - 8)
        final_col = self.col_dict[self.best_move[2]]

        initial_square = Square(initial_row, initial_col)
        final_square = Square(final_row, final_col)

        move = Move(initial_square, final_square)

        # get matching piece
        piece = board.squares[initial_row][initial_col].piece

        board.move(piece, move)

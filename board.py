import copy

from const import *
from square import Square
from piece import *
from move import Move
from config import Config



class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self._create()
        self.next_player = 'white'
        self.last_move = None
        self._add_pieces('white')
        self._add_pieces('black')
        self.config = Config()

    def _create(self):

        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def move(self, piece, move):

        initial = move.initial
        final = move.final

        if self.squares[final.row][final.col].has_piece():
            # piece.attacked = True
            self.config.capture_sound.play()

        else:
            self.config.move_sound.play()

        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        # check if move being moved is king castling
        if isinstance(piece, King):
            if self.is_castling(move):
                if isinstance(self.squares[final.row][final.col - 2].piece, Rook):
                    rook_initial = Square(final.row, final.col - 2)
                    rook_final = Square(final.row, final.col + 1)
                    rook_move = Move(rook_initial, rook_final)
                    self.move(self.squares[final.row][final.col - 2].piece, rook_move)
                elif isinstance(self.squares[final.row][final.col + 1].piece, Rook):
                    rook_initial = Square(final.row, final.col + 1)
                    rook_final = Square(final.row, final.col - 1)
                    rook_move = Move(rook_initial, rook_final)
                    self.move(self.squares[final.row][final.col + 1].piece, rook_move)

        # check if pawn is at promotion square
        if isinstance(piece, Pawn):
            if final.row == 0 or final.row == 7:
                self.squares[final.row][final.col] = Square(final.row, final.col, Queen(piece.color))

        piece.moved = True
        piece.clear_moves()

        self.last_move = move

    def is_castling(self, move):
        return abs(move.initial.col - move.final.col) == 2

    def output_moves(self, piece, move):

        key = [(0, 'h'),(1, 'g'),(2, 'f'),(3, 'e'),(4, 'd'),(5, 'c'),(6, 'b'),(7, 'a')]
        initial_row, initial_col = move.initial.row, move.initial.col
        final_row, final_col = move.final.row, move.final.col

        for elem in key:
            if initial_row == elem[0]:
                initial_row = elem[1]
            if final_row == elem[0]:
                final_row = elem[1]

        if piece.attacked:
            if piece.name == 'pawn':
                print('(', initial_row, 'x' , final_row, final_col + 1, ')' )
            else:
                name = 'n' if piece.name == 'knight' else piece.name[0]
                print('(', name, 'x', final_row, final_col + 1, ')')

            piece.attacked = False

        else:

            if piece.name == 'pawn':
                print('(', final_row, final_col + 1, ')' )
            else:
                name = 'n' if piece.name == 'knight' else piece.name[0]
                print('(', name, final_row, final_col + 1, ')')

    def is_valid_move(self, piece, move):
        if self.squares[move.final.row][move.final.col].piece:
            # if piece is trying to move to square with friendly piece
            if self.squares[move.final.row][move.final.col].piece.color == piece.color:
                return False
        if not self.will_expose_king(piece, move):
            return move in piece.moves
        else:
            return False

    def are_castling_squares_empty(self, piece, row, col, final_row, final_col):
        initial = Square(row, col)
        final = Square(final_row, final_col)
        empty = True

        if initial.col < final.col:
            for i in range(1, 3, 1):
                print(i)
                if self.squares[initial.row][initial.col + i].is_empty():
                    final = Square(initial.row, initial.col + i)
                    move = Move(initial, final)
                    if self.will_expose_king(piece, move):
                        empty = False
                else:
                    empty = False

        elif initial.col > final.col:
            for i in range(1, 4, 1):
                if self.squares[initial.row][initial.col - i].is_empty():
                    final = Square(initial.row, initial.col - i)
                    move = Move(initial, final)
                    if self.will_expose_king(piece, move):
                        empty = False
                else:
                    empty = False

        return empty

    def _add_pieces(self, color):

        pawn_row, piece_row = (6, 7) if color == 'white' else (1, 0)

        for col in range(COLS):  # set pawns
            self.squares[pawn_row][col] = Square(pawn_row, col, Pawn(color))

        print("break")
        self.squares[piece_row][0] = Square(piece_row, col, Rook(color))
        self.squares[piece_row][7] = Square(piece_row, col, Rook(color))

        self.squares[piece_row][1] = Square(piece_row, col, Knight(color))
        self.squares[piece_row][6] = Square(piece_row, col, Knight(color))

        self.squares[piece_row][2] = Square(piece_row, col, Bishop(color))
        self.squares[piece_row][5] = Square(piece_row, col, Bishop(color))

        self.squares[piece_row][3] = Square(piece_row, col, Queen(color))
        self.squares[piece_row][4] = Square(piece_row, col, King(color))

    def calc_moves(self, piece, row, col, testing=True):

        def knight_moves():

            possible_moves = [
                (row - 2, col + 1),
                (row - 1, col + 2),
                (row + 1, col + 2),
                (row + 2, col + 1),
                (row + 2, col - 1),
                (row + 1, col - 2),
                (row - 1, col - 2),
                (row - 2, col - 1),
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].is_empty_or_rival(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)

                        if testing:
                            if not self.will_expose_king(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

        def bishop_moves():

            possible_moves = [
                [
                    (row + 1, col + 1),
                    (row + 2, col + 2),
                    (row + 3, col + 3),
                    (row + 4, col + 4),
                    (row + 5, col + 5),
                    (row + 6, col + 6),
                    (row + 7, col + 7),
                ],
                [
                    (row - 1, col - 1),
                    (row - 2, col - 2),
                    (row - 3, col - 3),
                    (row - 4, col - 4),
                    (row - 5, col - 5),
                    (row - 6, col - 6),
                    (row - 7, col - 7),
                ],
                [
                    (row + 1, col - 1),
                    (row + 2, col - 2),
                    (row + 3, col - 3),
                    (row + 4, col - 4),
                    (row + 5, col - 5),
                    (row + 6, col - 6),
                    (row + 7, col - 7),
                ],
                [
                    (row - 1, col + 1),
                    (row - 2, col + 2),
                    (row - 3, col + 3),
                    (row - 4, col + 4),
                    (row - 5, col + 5),
                    (row - 6, col + 6),
                    (row - 7, col + 7),
                ],
            ]

            for diagonal in possible_moves:
                for possible_move in diagonal:

                    possible_move_row, possible_move_col = possible_move

                    if Square.in_range(possible_move_row, possible_move_col):  # make sure moves are in range

                        if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):  # if square has team piece, move onto next diagonal
                            break

                        if self.squares[possible_move_row][possible_move_col].is_empty_or_rival(piece.color):
                            # if square is empty or contains rival piece, add move
                            initial = Square(row, col)
                            final = Square(possible_move_row, possible_move_col)
                            move = Move(initial, final)
                            if testing:
                                if not self.will_expose_king(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)

                        if self.squares[possible_move_row][possible_move_col].has_piece():  # if square has rival piece, move onto next diagonal, after adding potential attack move
                            break

        def king_moves():

            possible_moves = [
                (row - 1, col - 1),
                (row - 1, col),
                (row + 1, col),
                (row, col - 1),
                (row, col + 1),
                (row - 1, col + 1),
                (row + 1, col - 1),
                (row + 1, col + 1),
            ]

            castling_moves = [
                (row, col + 2, 7, 7, 'white'),
                (row, col - 2, 7, 0, 'white'),
                (row, col + 2, 0, 7, 'black'),
                (row, col - 2, 0, 0, 'black'),
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].is_empty_or_rival(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        if testing:
                            if not self.will_expose_king(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

            if testing:
                if not piece.moved:
                    for possible_move in castling_moves:
                        possible_move_row, possible_move_col, rook_row, rook_col, piece_color = possible_move

                        if piece_color == piece.color:
                            if isinstance(self.squares[rook_row][rook_col].piece, Rook):
                                 if not self.squares[rook_row][rook_col].piece.moved:
                                    # if castling squares are empty
                                    if self.are_castling_squares_empty(piece, row, col, possible_move_row, possible_move_col):
                                        # add king move
                                        initial = Square(row, col)
                                        final = Square(possible_move_row, possible_move_col)
                                        move = Move(initial, final)
                                        if not self.will_expose_king(piece, move):
                                            piece.add_move(move)

        def rook_moves():

            possible_moves = [
                [
                    (row + 1, col),
                    (row + 2, col),
                    (row + 3, col),
                    (row + 4, col),
                    (row + 5, col),
                    (row + 6, col),
                    (row + 7, col)
                ],
                [
                    (row - 1, col),
                    (row - 2, col),
                    (row - 3, col),
                    (row - 4, col),
                    (row - 5, col),
                    (row - 6, col),
                    (row - 7, col),
                ],
                [
                    (row, col + 1),
                    (row, col + 2),
                    (row, col + 3),
                    (row, col + 4),
                    (row, col + 5),
                    (row, col + 6),
                    (row, col + 7),
                ],
                [
                    (row, col - 1),
                    (row, col - 2),
                    (row, col - 3),
                    (row, col - 4),
                    (row, col - 5),
                    (row, col - 6),
                    (row, col - 7),
                ]
            ]

            for rank in possible_moves:
                for possible_move in rank:

                    possible_move_row, possible_move_col = possible_move

                    if Square.in_range(possible_move_row, possible_move_col):  # make sure moves are in range

                        if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):  # if square has team piece, move onto next diagonal
                            break

                        if self.squares[possible_move_row][possible_move_col].is_empty_or_rival(piece.color):  # if square is empty or contains rival piece, add move
                            initial = Square(row, col)
                            final = Square(possible_move_row, possible_move_col)
                            move = Move(initial, final)
                            if testing:
                                if not self.will_expose_king(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)

                        if self.squares[possible_move_row][possible_move_col].has_piece():  # if square has rival piece, move onto next diagonal, after adding potential attack move
                            break

        def queen_moves():

            possible_rank_moves = [
                [
                    (row + 1, col + 1),
                    (row + 2, col + 2),
                    (row + 3, col + 3),
                    (row + 4, col + 4),
                    (row + 5, col + 5),
                    (row + 6, col + 6),
                    (row + 7, col + 7),
                ],
                [
                    (row - 1, col - 1),
                    (row - 2, col - 2),
                    (row - 3, col - 3),
                    (row - 4, col - 4),
                    (row - 5, col - 5),
                    (row - 6, col - 6),
                    (row - 7, col - 7),
                ],
                [
                    (row + 1, col - 1),
                    (row + 2, col - 2),
                    (row + 3, col - 3),
                    (row + 4, col - 4),
                    (row + 5, col - 5),
                    (row + 6, col - 6),
                    (row + 7, col - 7),
                ],
                [
                    (row - 1, col + 1),
                    (row - 2, col + 2),
                    (row - 3, col + 3),
                    (row - 4, col + 4),
                    (row - 5, col + 5),
                    (row - 6, col + 6),
                    (row - 7, col + 7),
                ],
                [
                    (row + 1, col),
                    (row + 2, col),
                    (row + 3, col),
                    (row + 4, col),
                    (row + 5, col),
                    (row + 6, col),
                    (row + 7, col)
                ],
                [
                    (row - 1, col),
                    (row - 2, col),
                    (row - 3, col),
                    (row - 4, col),
                    (row - 5, col),
                    (row - 6, col),
                    (row - 7, col),
                ],
                [
                    (row, col + 1),
                    (row, col + 2),
                    (row, col + 3),
                    (row, col + 4),
                    (row, col + 5),
                    (row, col + 6),
                    (row, col + 7),
                ],
                [
                    (row, col - 1),
                    (row, col - 2),
                    (row, col - 3),
                    (row, col - 4),
                    (row, col - 5),
                    (row, col - 6),
                    (row, col - 7),
                ]
            ]

            for rank in possible_rank_moves:
                for possible_move in rank:
                    possible_move_row, possible_move_col = possible_move

                    if Square.in_range(possible_move_row, possible_move_col):  # make sure moves are in range

                        if self.squares[possible_move_row][possible_move_col].has_team_piece(
                                piece.color):  # if square has team piece, move onto next diagonal
                            break

                        if self.squares[possible_move_row][possible_move_col].is_empty_or_rival(piece.color):  # if square is empty or contains rival piece, add move
                            initial = Square(row, col)
                            final = Square(possible_move_row, possible_move_col)
                            move = Move(initial, final)
                            if testing:
                                if not self.will_expose_king(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)

                        if self.squares[possible_move_row][possible_move_col].has_piece(): # if square has rival piece, move onto next diagonal, after adding potential attack move
                            break

        def pawn_moves():

            steps = 1 if piece.moved else 2

            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for move_row in range(start, end, piece.dir):
                if Square.in_range(move_row):
                    if self.squares[move_row][col].is_empty():
                        initial = Square(row, col)
                        final = Square(move_row, col)
                        move = Move(initial, final)
                        if testing:
                            if not self.will_expose_king(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

                    else:
                        break
                else:
                    break

            possible_move_row = row + piece.dir
            possible_move_cols = [col - 1, col + 1]

            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row,possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        if testing:
                            if not self.will_expose_king(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

        if isinstance(piece, Queen):
            queen_moves()

        elif isinstance(piece, Knight):
            knight_moves()

        elif isinstance(piece, Bishop):
            bishop_moves()

        elif isinstance(piece, King):
            king_moves()

        elif isinstance(piece, Rook):
            rook_moves()

        elif isinstance(piece, Pawn):
            pawn_moves()

    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def get_king_position(self,color):

        for row in range(0, 8, 1):
            for col in range(0, 8, 1):
                if isinstance(self.squares[row][col].piece, King):
                    if self.squares[row][col].piece.color == color:
                        return row, col

    def calc_rival_moves(self, color, testing=False):
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_piece():
                    if self.squares[row][col].piece.color != color:
                        self.calc_moves(self.squares[row][col].piece, row, col, False)

    def clear_rival_moves(self, color):

        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_piece():
                    if self.squares[row][col].piece.color != color:
                        self.squares[row][col].piece.moves = []

    def will_expose_king(self, piece, move):
        # temporarily move pending piece on board, then reset board when finished

        # find position of king
        if piece.name != 'king':
            king_row, king_col = self.get_king_position(piece.color)
        else:
            king_row, king_col = move.final.row, move.final.col

        empty = True
        attacked = False

        # if final move square has rival piece, save it to restore, place pending piece
        if self.squares[move.final.row][move.final.col].has_rival_piece(piece.color):
            temp_piece = self.squares[move.final.row][move.final.col].piece
            self.squares[move.final.row][move.final.col].piece = piece
            self.squares[move.initial.row][move.initial.col].piece = None
            empty = False

        # if square is empty, place pending piece there and remove it from current spot
        elif self.squares[move.final.row][move.final.col].is_empty():
            self.squares[move.final.row][move.final.col].piece = piece
            self.squares[move.initial.row][move.initial.col].piece = None

        # calculate all enemy moves
        self.clear_rival_moves(piece.color)
        self.calc_rival_moves(piece.color, False)

        # check all opposing pieces potential moves
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_piece():
                    if self.squares[row][col].piece.color != piece.color:
                        enemy_piece = self.squares[row][col].piece
                        for possible_moves in enemy_piece.moves:
                            if possible_moves.final.row == king_row and possible_moves.final.col == king_col:
                                # if king will be attacked as a result, return True
                                attacked = True

        # replace removed piece if square was not empty
        if not empty:
            self.squares[move.final.row][move.final.col].piece = temp_piece
        # remove pending piece from final move square
        else:
            self.squares[move.final.row][move.final.col].piece = None

        # restore pending piece
        self.squares[move.initial.row][move.initial.col].piece = piece

        # clear moves
        self.clear_rival_moves(piece.color)

        return attacked

    def is_game_over(self):

        # after a color moves, see if opposing color has any valid moves
        color = 'white' if self.next_player == 'black' else 'black'

        # calculate opposing color moves
        self.calc_rival_moves(self.next_player)

        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_piece():
                    # find all opposing pieces
                    if self.squares[row][col].piece.color == color:
                        # check for any valid move between all pieces
                        for move in self.squares[row][col].piece.moves:
                            if not self.will_expose_king(self.squares[row][col].piece, move):
                                return False

        print('Game over,', self.next_player, 'wins!')
        return True

    def castling_options(self):
        options = ""

        if isinstance(self.squares[7][4].piece, King):
            if not self.squares[7][4].piece.moved:
                if isinstance(self.squares[7][7].piece, Rook):
                    if not self.squares[7][7].piece.moved:
                        options += "K"
                if isinstance(self.squares[7][0].piece, Rook):
                    if not self.squares[7][0].piece.moved:
                        if not self.squares[7][0].piece.moved:
                            options += "Q"

        if isinstance(self.squares[0][4].piece, King):
            if not self.squares[0][4].piece.moved:
                if isinstance(self.squares[0][0].piece, Rook):
                    if not self.squares[0][0].piece.moved:
                        options += "q"
                if isinstance(self.squares[0][7].piece, Rook):
                    if not self.squares[0][7].piece.moved:
                        if not self.squares[0][0].piece.moved:
                            options += "k"

        return options
















import os

class Piece:

    def __init__(self, name, color, texture=None, texture_rect=None):
        self.name = name
        self.color = color
        self.moved = False
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect
        self.moves = []
        self.attacked = False
        self.castling = False

    def set_texture(self):

        piece_color = 'b' if self.color == 'black' else 'w'

        if self.name == 'bishop':
            piece_name = 'b'

        elif self.name == 'pawn':
            piece_name = 'p'

        elif self.name == 'rook':
            piece_name = 'r'

        elif self.name == 'queen':
            piece_name = 'q'

        elif self.name == 'king':
            piece_name = 'k'

        elif self.name == 'knight':
            piece_name = 'n'

        self.texture = os.path.join(f'assets/icons/{piece_name}{piece_color}.png')

    def add_move(self, move):
        self.moves.append(move)

    def clear_moves(self):
        self.moves = []


class Pawn(Piece):

    def __init__(self, color):
        self.dir = -1 if color == 'white' else 1
        super().__init__('pawn', color)


class Knight(Piece):

    def __init__(self, color):
        super().__init__('knight', color)


class Bishop(Piece):

    def __init__(self, color):
        super().__init__('bishop', color)


class Rook(Piece):

    def __init__(self, color):
        super().__init__('rook', color)


class Queen(Piece):

    def __init__(self, color):
        super().__init__('queen', color)


class King(Piece):

    def __init__(self, color):
        super().__init__('king', color)



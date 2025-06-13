class Square:
    COLS = 'abcdefgh'

    def __init__(self, row, col, piece=None):
        self.row, self.col, self.piece = row, col, piece
        self.alphacol = Square.COLS[col]

    def __eq__(self, other):
        return (self.row, self.col) == (other.row, other.col)

    def has_piece(self):
        return self.piece is not None

    def isempty(self):
        return self.piece is None

    def has_team_piece(self, color):
        return self.piece and self.piece.color == color

    def has_enemy_piece(self, color):
        return self.piece and self.piece.color != color

    def isempty_or_enemy(self, color):
        return not self.piece or self.piece.color != color

    @staticmethod
    def in_range(*args):
        return all(0 <= arg <= 7 for arg in args)

    @staticmethod
    def get_alphacol(col):
        return Square.COLS[col]
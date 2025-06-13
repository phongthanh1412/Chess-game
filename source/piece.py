import os

class Piece:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.moves = []
        self.moved = False
        self.texture = self.set_texture()
        self.texture_rect = None

    def set_texture(self):
        self.texture = os.path.join('assets/images', f'{self.color}_{self.name}.png')


    def add_move(self, move):
        self.moves.append(move)

    def clear_moves(self):
        self.moves.clear()

class Pawn(Piece):
    def __init__(self, color):
        super().__init__('pawn', color)
        self.direction = -1 if color == 'white' else 1
        self.en_passant = False

class Knight(Piece):  
    def __init__(self, color): super().__init__('knight', color)

class Bishop(Piece):  
    def __init__(self, color): super().__init__('bishop', color)

class Rook(Piece):    
    def __init__(self, color): super().__init__('rook', color)

class Queen(Piece):   
    def __init__(self, color): super().__init__('queen', color)

class King(Piece):
    def __init__(self, color):
        super().__init__('king', color)
        self.left_rook = None
        self.right_rook = None
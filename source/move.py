class Move:
    def __init__(self, initial, final):
        self.initial, self.final = initial, final

    def __str__(self):
        return f'({self.initial.col}, {self.initial.row}) -> ({self.final.col}, {self.final.row})'

    def __eq__(self, other):
        return isinstance(other, Move) and self.initial == other.initial and self.final == other.final
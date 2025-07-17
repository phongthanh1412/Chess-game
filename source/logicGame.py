import copy
import pygame
import datetime
from CONSTANT import *
from square import Square
from piece import *
from move import Move
from setting import Sound
from promotion import choose_promotion, promote_to

class Board:
    def __init__(self):
        self.squares = [[Square(row, col) for col in range(COLS)] for row in range(ROWS)]
        self.last_move = None
        self.en_passant = None
        self.move_history = []  # Store move history as dictionary
        self.pgn_moves = []     # Store move history in SAN format
        self.move_count = 0     # Count total moves
        self.full_move_number = 1  # Move number for PGN
        self.half_move_number = 0  # Count half-moves without capture or pawn move
        self.game_result = ""  # Game result: "1-0", "0-1", "1/2-1/2"
        self._add_pieces('white')
        self._add_pieces('black')

    def move(self, piece, move, testing=False,promotion_choice = None):
        initial, final = move.initial, move.final
        en_passant_empty = self.squares[final.row][final.col].isempty()

        # Store state before moving
        move_state = {
            'piece': type(piece).__name__,
            'color': piece.color,
            'from': (initial.row, initial.col),
            'to': (final.row, final.col),
            'captured': self.squares[final.row][final.col].has_piece(),
            'en_passant': False,
            'pawn_move': isinstance(piece, Pawn),
            'promotion': None,
            'castling': None,
            'check': False,
            'checkmate': False
        }

        # Update board
        captured_piece = self.squares[final.row][final.col].piece
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        # Handle special moves
        if isinstance(piece, Pawn):
            if (diff := final.col - initial.col) != 0 and en_passant_empty:
                self.squares[initial.row][initial.col + diff].piece = None
                move_state['captured'] = True
                move_state['en_passant'] = True
            
            if final.row in (0, 7):
                if not testing:
                    if promotion_choice is None:
                        screen = pygame.display.get_surface()
                        choice = choose_promotion(screen, piece.color)
                    else:
                        choice = promotion_choice
                    promoted_piece = promote_to(choice, piece.color)
                else:
                    promoted_piece = Queen(piece.color)
                promoted_piece.moved = True
                promoted_piece.promoted_from_pawn = True
                self.squares[final.row][final.col].piece = promoted_piece
                move_state['promotion'] = type(promoted_piece).__name__
                move_state['piece'] = type(promoted_piece).__name__

        elif isinstance(piece, King) and abs(initial.col - final.col) == 2:
            move_state['castling'] = 'kingside' if final.col > initial.col else 'queenside'
            if not testing:
                self._handle_castling(piece, initial, final)
                Sound(CASTLE_SOUND).play()
        # Finalize move
        piece.moved = True
        piece.clear_moves()
        self.last_move = move
        
        # Check for check and checkmate
        if not testing:
            opponent_color = 'black' if piece.color == 'white' else 'white'
            king_pos = self._find_king(opponent_color)
            if king_pos:
                move_state['check'] = self._is_king_in_check(opponent_color, king_pos)
                move_state['checkmate'] = self.is_checkmate(opponent_color)
        # Handle sounds
        if not testing:
            if move_state['checkmate']:
                Sound(CHECKMATE_SOUND).play()
            elif move_state['check']:
                Sound(CHECK_SOUND).play()
            elif move_state['captured'] or move_state['en_passant']:
                Sound(CAPTURE_SOUND).play()
            elif not move_state['castling']:
                Sound(MOVE_SOUND).play()
        # Convert move to SAN
        if not testing:
            san = self._to_san(piece, move, move_state, captured_piece)
            if piece.color == 'white':
                self.pgn_moves.append(f"{self.full_move_number}. {san}")
            else:
                self.pgn_moves[-1] += f" {san}"

        # Update history and move counters
        if not testing:
            self.move_history.append(move_state)
            self.move_count += 1
            if piece.color == 'black':
                self.full_move_number += 1  # Increment move number after black's turn

            # Update half-move clock
            if move_state['captured'] or move_state['pawn_move']:
                self.half_move_number = 0
            else:
                self.half_move_number += 1

    def _to_san(self, piece, move, move_state, captured_piece):
        """Convert move to SAN notation."""
        initial, final = move.initial, move.final
        col_to_file = COL_PIECE
        row_to_rank = ROW_PIECE
        piece_symbol = '' if isinstance(piece, Pawn) else {'King': 'K', 'Queen': 'Q', 'Rook': 'R', 'Bishop': 'B', 'Knight': 'N'}[type(piece).__name__]

        # Handle castling
        if move_state['castling']:
            return 'O-O' if move_state['castling'] == 'kingside' else 'O-O-O'

        # Build basic notation
        to_square = f"{col_to_file[final.col]}{row_to_rank[final.row]}"
        capture = 'x' if move_state['captured'] or move_state['en_passant'] else ''
        san = ''

        # Handle pawn moves
        if isinstance(piece, Pawn):
            if capture:
                san = f"{col_to_file[initial.col]}{capture}{to_square}"
            else:
                san = to_square
            if move_state['promotion']:
                san += f"={'QRNB'[{'Queen': 0, 'Rook': 1, 'Knight': 2, 'Bishop': 3}[move_state['promotion']]]}"
        else:
            # Disambiguate if needed
            ambiguity = []
            for row in range(ROWS):
                for col in range(COLS):
                    other = self.squares[row][col].piece
                    if other and other != piece and other.color == piece.color and type(other) == type(piece):
                        self.calc_moves(other, row, col, bool=False)
                        if any(m.final.row == final.row and m.final.col == final.col for m in other.moves):
                            ambiguity.append((row, col))
            
            disambiguate = ''
            if ambiguity:
                same_file = any(initial.col == pos[1] for pos in ambiguity)
                same_rank = any(initial.row == pos[0] for pos in ambiguity)
                if same_file and same_rank:
                    disambiguate = f"{col_to_file[initial.col]}{row_to_rank[initial.row]}"
                elif same_file:
                    disambiguate = row_to_rank[initial.row]
                else:
                    disambiguate = col_to_file[initial.col]
            
            san = f"{piece_symbol}{disambiguate}{capture}{to_square}"

        # Add check or checkmate symbols
        if move_state['checkmate']:
            san += '#'
        elif move_state['check']:
            san += '+'

        return san

    def save_pgn_to_file(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"game_{timestamp}.txt"
        
        # Create PGN headers
        headers = [
            '[Event: Norway Chess]',
            '[Date: {}]'.format(datetime.datetime.now().strftime("%Y.%m.%d")),
            '[White: Player1]',
            '[Black: Player2]',
            '[Result: {}]'.format(self.game_result)
        ]

        # Format move list
        pgn_text = '\n'.join(headers) + '\n\n'
        pgn_text += '\n'.join(self.pgn_moves)

        # Write to file
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(pgn_text)
        except Exception:
            pass

    def is_insufficient_material(self):
        """Check for delta_draw due to insufficient material."""
        pieces = []
        for row in self.squares:
            for square in row:
                if square.has_piece():
                    pieces.append(square.piece)
        
        if len(pieces) <= 2:  # Only two kings
            self.game_result = "1/2-1/2"
            return True
        if len(pieces) == 3:  # King vs King + Bishop/Knight
            for piece in pieces:
                if isinstance(piece, (Bishop, Knight)):
                    self.game_result = "1/2-1/2"
                    return True
        return False

    def is_threefold_repetition(self):
        if len(self.move_history) < 12:
            return False

        last_twelve_moves = self.move_history[-12:]
        colors = [move['color'] for move in last_twelve_moves]
        expected_colors = ['black', 'white', 'black', 'white'] * 3
        alternate_colors = ['white', 'black', 'white', 'black'] * 3
        if colors != expected_colors and colors != alternate_colors:
            return False

        cycles = [last_twelve_moves[i:i+4] for i in range(0, 12, 4)]
        cycle_1 = cycles[0]
        if len(cycle_1) != 4:
            return False

        move_A_forward = cycle_1[0]
        move_B_forward = cycle_1[1]
        move_A_backward = cycle_1[2]
        move_B_backward = cycle_1[3]

        if not (move_A_forward['to'] == move_A_backward['from'] and
                move_A_backward['to'] == move_A_forward['from'] and
                move_B_forward['to'] == move_B_backward['from'] and
                move_B_backward['to'] == move_B_forward['from']):
            return False

        for cycle in cycles[1:]:
            if len(cycle) != 4:
                return False
            if not (cycle[0]['piece'] == move_A_forward['piece'] and
                    cycle[0]['from'] == move_A_forward['from'] and
                    cycle[0]['to'] == move_A_forward['to'] and
                    cycle[1]['piece'] == move_B_forward['piece'] and
                    cycle[1]['from'] == move_B_forward['from'] and
                    cycle[1]['to'] == move_B_forward['to'] and
                    cycle[2]['piece'] == move_A_backward['piece'] and
                    cycle[2]['from'] == move_A_backward['from'] and
                    cycle[2]['to'] == move_A_backward['to'] and
                    cycle[3]['piece'] == move_B_backward['piece'] and
                    cycle[3]['from'] == move_B_backward['from'] and
                    cycle[3]['to'] == move_B_backward['to']):
                return False

        self.game_result = "1/2-1/2"
        return True

    def is_fifty_move_rule(self):
        """Check for 50-move rule."""
        if self.half_move_number >= FIFTY_MOVES:
            self.game_result = "1/2-1/2"
            return True
        return False

    def is_stalemate(self, color):
        """Check for stalemate."""
        king_pos = self._find_king(color)
        if not king_pos:
            return False

        if self._is_king_in_check(color, king_pos):
            return False

        for row in self.squares:
            for square in row:
                piece = square.piece
                if piece and piece.color == color:
                    self.calc_moves(piece, square.row, square.col, bool=True)
                    if piece.moves:
                        return False
        self.game_result = "1/2-1/2"
        return True

    def is_checkmate(self, color):
        """Check for checkmate."""
        king_pos = self._find_king(color)
        if not king_pos:
            return False

        if not self._is_king_in_check(color, king_pos):
            return False

        king = self.squares[king_pos.row][king_pos.col].piece
        self.calc_moves(king, king_pos.row, king_pos.col, bool=True)
        if king.moves:
            return False

        attackers = self._get_attacking_pieces(king_pos, color)

        attacker_pos = attackers[0]
        attacker = self.squares[attacker_pos.row][attacker_pos.col].piece

        if self._can_capture_attacker(attacker_pos, color):
            return False

        if self._can_block_attack(king_pos, attacker_pos, color):
            return False

        self.game_result = "1-0" if color == 'black' else "0-1"
        return True

    def is_draw(self, color):
        """Check delta_draw conditions."""
        return (self.is_stalemate(color) or 
                self.is_threefold_repetition() or 
                self.is_fifty_move_rule() or
                self.is_insufficient_material())

    def valid_move(self, piece, move):
        return move in piece.moves

    def set_true_en_passant(self, piece):
        if isinstance(piece, Pawn):
            for row in self.squares:
                for square in row:
                    if isinstance(square.piece, Pawn):
                        square.piece.en_passant = False
            piece.en_passant = True

    def in_check(self, piece, move):
        temp = copy.deepcopy(self)
        temp.move(copy.deepcopy(piece), move, testing=True)
        
        for row in temp.squares:
            for square in row:
                if square.has_enemy_piece(piece.color):
                    enemy = square.piece
                    temp.calc_moves(enemy, square.row, square.col, bool=False)
                    if any(isinstance(m.final.piece, King) and m.final.piece.color == piece.color for m in enemy.moves):
                        return True
        return False

    def calc_moves(self, piece, row, col, bool=True):
        piece.clear_moves()
        
        if isinstance(piece, Pawn):
            self._calc_pawn_moves(piece, row, col, bool)
        elif isinstance(piece, Knight):
            self._calc_knight_moves(piece, row, col, bool)
        elif isinstance(piece, Bishop):
            self._calc_bishop_moves(piece, row, col, bool)
        elif isinstance(piece, Rook):
            self._calc_rook_moves(piece, row, col, bool)
        elif isinstance(piece, Queen):
            self._calc_queen_moves(piece, row, col, bool)
        elif isinstance(piece, King):
            self._calc_king_moves(piece, row, col, bool)

    def _calc_pawn_moves(self, piece, row, col, bool):
        steps = 1 if piece.moved else 2
        for step in range(1, steps + 1):
            move_row = row + piece.direction * step
            if not Square.in_range(move_row) or not self.squares[move_row][col].isempty():
                break
            self._add_valid_move(piece, row, col, move_row, col, bool)

        for delta_col in (-1, 1):
            move_row, move_col = row + piece.direction, col + delta_col
            if Square.in_range(move_row, move_col) and self.squares[move_row][move_col].has_enemy_piece(piece.color):
                self._add_valid_move(piece, row, col, move_row, move_col, bool)

        r, fr = (3, 2) if piece.color == 'white' else (4, 5)
        if row == r:
            for delta_col in (-1, 1):
                if Square.in_range(col + delta_col) and self.squares[row][col + delta_col].has_enemy_piece(piece.color):
                    p = self.squares[row][col + delta_col].piece
                    if isinstance(p, Pawn) and p.en_passant:
                        self._add_valid_move(piece, row, col, fr, col + delta_col, bool, p)

    def _calc_knight_moves(self, piece, row, col, bool):
        for delta_row, delta_col in [(-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1)]:
            self._add_move_if_valid(piece, row, col, row + delta_row, col + delta_col, bool)

    def _calc_bishop_moves(self, piece, row, col, bool):
        increments = [(-1, 1), (-1, -1), (1, 1), (1, -1)]
        self._calc_straightline_moves(piece, row, col, increments, bool)

    def _calc_rook_moves(self, piece, row, col, bool):
        increments = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        self._calc_straightline_moves(piece, row, col, increments, bool)

    def _calc_queen_moves(self, piece, row, col, bool):
        increments = [(-1, 1), (-1, -1), (1, 1), (1, -1), (-1, 0), (0, 1), (1, 0), (0, -1)]
        self._calc_straightline_moves(piece, row, col, increments, bool)

    def _calc_straightline_moves(self, piece, row, col, increments, bool):
        for delta_row, delta_col in increments:
            new_row, new_col = row + delta_row, col + delta_col
            while Square.in_range(new_row, new_col):
                if self.squares[new_row][new_col].isempty():
                    self._add_valid_move(piece, row, col, new_row, new_col, bool)
                elif self.squares[new_row][new_col].has_enemy_piece(piece.color):
                    self._add_valid_move(piece, row, col, new_row, new_col, bool)
                    break
                else:
                    break
                new_row += delta_row
                new_col += delta_col

    def _calc_king_moves(self, piece, row, col, bool):
        for delta_row in (-1, 0, 1):
            for delta_col in (-1, 0, 1):
                if delta_row == delta_col == 0:
                    continue
                self._add_move_if_valid(piece, row, col, row + delta_row, col + delta_col, bool)

        if not piece.moved:
            if self._can_castle_queenside(piece, row, bool):
                self._add_queenside_castling(piece, row, col, bool)
            if self._can_castle_kingside(piece, row, bool):
                self._add_kingside_castling(piece, row, col, bool)

    def _can_castle_queenside(self, piece, row, bool):
        if not self.squares[row][0].piece or not isinstance(self.squares[row][0].piece, Rook):
            return False
        rook = self.squares[row][0].piece
        if rook.moved:
            return False
        for c in [1, 2, 3]:
            if self.squares[row][c].has_piece():
                return False
        if bool:
            for col in [4, 3, 2]:
                move = Move(Square(row, 4), Square(row, col))
                if self.in_check(piece, move):
                    return False
        return True

    def _can_castle_kingside(self, piece, row, bool):
        if not self.squares[row][7].piece or not isinstance(self.squares[row][7].piece, Rook):
            return False
        rook = self.squares[row][7].piece
        if rook.moved:
            return False
        for c in [5, 6]:
            if self.squares[row][c].has_piece():
                return False
        if bool:
            for col in [4, 5, 6]:
                move = Move(Square(row, 4), Square(row, col))
                if self.in_check(piece, move):
                    return False
        return True

    def _add_queenside_castling(self, piece, row, col, bool):
        rook = self.squares[row][0].piece
        piece.left_rook = rook
        rook_move = Move(Square(row, 0), Square(row, 3))
        king_move = Move(Square(row, col), Square(row, 2))
        
        if not bool or not self.in_check(piece, king_move):
            rook.add_move(rook_move)
            piece.add_move(king_move)

    def _add_kingside_castling(self, piece, row, col, bool):
        rook = self.squares[row][7].piece
        piece.right_rook = rook
        rook_move = Move(Square(row, 7), Square(row, 5))
        king_move = Move(Square(row, col), Square(row, 6))
        
        if not bool or not self.in_check(piece, king_move):
            rook.add_move(rook_move)
            piece.add_move(king_move)

    def _add_move_if_valid(self, piece, row, col, move_row, move_col, bool):
        if Square.in_range(move_row, move_col) and self.squares[move_row][move_col].isempty_or_enemy(piece.color):
            self._add_valid_move(piece, row, col, move_row, move_col, bool)

    def _add_valid_move(self, piece, row, col, move_row, move_col, bool, final_piece=None):
        final_piece = final_piece or self.squares[move_row][move_col].piece
        move = Move(Square(row, col), Square(move_row, move_col, final_piece))
        if not bool or not self.in_check(piece, move):
            piece.add_move(move)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)
        
        for col in range(COLS):
            self.squares[row_pawn][col].piece = Pawn(color)

        pieces = [
            (Rook, [(row_other, 0), (row_other, 7)]),
            (Knight, [(row_other, 1), (row_other, 6)]),
            (Bishop, [(row_other, 2), (row_other, 5)]),
            (Queen, [(row_other, 3)]),
            (King, [(row_other, 4)])
        ]

        for piece_type, positions in pieces:
            for row, col in positions:
                self.squares[row][col].piece = piece_type(color)

    def _find_king(self, color):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.squares[row][col].piece
                if isinstance(piece, King) and piece.color == color:
                    return Square(row, col)
        return None

    def _is_king_in_check(self, color, king_pos):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.squares[row][col].piece
                if piece and piece.color != color:
                    self.calc_moves(piece, row, col, bool=False)
                    for move in piece.moves:
                        if move.final.row == king_pos.row and move.final.col == king_pos.col:
                            return True
        return False

    def _get_attacking_pieces(self, king_pos, color):
        attackers = []
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.squares[row][col].piece
                if piece and piece.color != color:
                    self.calc_moves(piece, row, col, bool=False)
                    for move in piece.moves:
                        if move.final.row == king_pos.row and move.final.col == king_pos.col:
                            attackers.append(Square(row, col))
        return attackers

    def _can_capture_attacker(self, attacker_pos, color):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.squares[row][col].piece
                if piece and piece.color == color:
                    self.calc_moves(piece, row, col, bool=True)
                    for move in piece.moves:
                        if move.final.row == attacker_pos.row and move.final.col == attacker_pos.col:
                            return True
        return False

    def _can_block_attack(self, king_pos, attacker_pos, color):
        path = self._get_attack_path(king_pos, attacker_pos)
        
        for square in path:
            for row in range(ROWS):
                for col in range(COLS):
                    piece = self.squares[row][col].piece
                    if piece and piece.color == color and not isinstance(piece, King):
                        self.calc_moves(piece, row, col, bool=True)
                        for move in piece.moves:
                            if move.final.row == square.row and move.final.col == square.col:
                                return True
        return False

    def _get_attack_path(self, king_pos, attacker_pos):
        path = []
        
        if king_pos.row == attacker_pos.row:
            step = 1 if attacker_pos.col < king_pos.col else -1
            for col in range(attacker_pos.col + step, king_pos.col, step):
                path.append(Square(king_pos.row, col))
                
        elif king_pos.col == attacker_pos.col:
            step = 1 if attacker_pos.row < king_pos.row else -1
            for row in range(attacker_pos.row + step, king_pos.row, step):
                path.append(Square(row, king_pos.col))
                
        elif abs(king_pos.row - attacker_pos.row) == abs(king_pos.col - attacker_pos.col):
            row_step = 1 if attacker_pos.row < king_pos.row else -1
            col_step = 1 if attacker_pos.col < king_pos.col else -1
            row, col = attacker_pos.row + row_step, attacker_pos.col + col_step
            while row != king_pos.row and col != king_pos.col:
                path.append(Square(row, col))
                row += row_step
                col += col_step
                
        return path

    def _handle_castling(self, piece, initial, final):
        if abs(initial.col - final.col) == 2:
            rook = piece.left_rook if final.col < initial.col else piece.right_rook
            if rook:
                self.move(rook, rook.moves[-1], testing=True)
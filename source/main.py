import pygame
import sys
from CONSTANT import *
from gameplaychess import ChessGame
from square import Square
from move import Move
from gameOver import show_result_popup  

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Chess Game')
    clock = pygame.time.Clock()

    game = ChessGame()
    board = game.board
    dragger = game.dragger

    game_over = False
    game_result = ""  # Store "checkmate", "stalemate", "repetition", "50-move", "insufficient", "resignation"
    popup_shown = False

    while True:
        # Clear screen
        screen.fill((0, 0, 0))

        # Draw the board
        game.draw_board(screen)
        game.draw_last_move(screen)
        if not game_over:  # Only show valid moves if game is ongoing
            game.draw_valid_moves(screen)
        game.draw_pieces(screen)
        
        if dragger.state['is_dragging']:
            dragger.render(screen)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                board.save_pgn_to_file()  # Save move history when quit
                pygame.quit()
                sys.exit()

            if game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:  # New game
                        board.save_pgn_to_file()  # Save move history before reset
                        game = ChessGame()
                        board = game.board
                        dragger = game.dragger
                        game_over = False
                        popup_shown = False
                        game_result = ""
                    elif event.key == pygame.K_q:  # Exit game
                        board.save_pgn_to_file()  # Save move history 
                        pygame.quit()
                        sys.exit()
                continue

            # Mouse down
            if event.type == pygame.MOUSEBUTTONDOWN:
                dragger.set_mouse_pos(event.pos)
                row = dragger.state['mouse_y'] // SQUARE_SIZE
                col = dragger.state['mouse_x'] // SQUARE_SIZE
                if board.squares[row][col].has_piece():
                    piece = board.squares[row][col].piece
                    if piece.color == game.state['current_player']:
                        board.calc_moves(piece, row, col, bool=True)
                        dragger.set_start_square(event.pos)
                        dragger.start_dragging(piece)

            # Mouse motion
            elif event.type == pygame.MOUSEMOTION:
                row = event.pos[1] // SQUARE_SIZE
                col = event.pos[0] // SQUARE_SIZE
                if dragger.state['is_dragging']:
                    dragger.set_mouse_pos(event.pos)

            # Mouse up
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragger.state['is_dragging']:
                    dragger.set_mouse_pos(event.pos)
                    start = Square(dragger.state['start_row'], dragger.state['start_col'])
                    end_row = dragger.state['mouse_y'] // SQUARE_SIZE
                    end_col = dragger.state['mouse_x'] // SQUARE_SIZE
                    end = Square(end_row, end_col)
                    move = Move(start, end)

                    if board.valid_move(dragger.state['piece'], move):
                        board.move(dragger.state['piece'], move)
                        board.set_true_en_passant(dragger.state['piece'])
                        game.switch_turn()

                        next_player = game.state['current_player']
                        if board.is_checkmate(next_player):
                            game_over = True
                            game_result = "checkmate"
                            popup_shown = True
                            board.game_result = "1-0" if next_player == 'black' else "0-1"
                        elif board.is_stalemate(next_player):
                            game_over = True
                            game_result = "stalemate"
                            popup_shown = True
                        elif board.is_threefold_repetition():
                            game_over = True
                            game_result = "repetition"
                            popup_shown = True
                        elif board.is_fifty_move_rule():
                            game_over = True
                            game_result = "50-move"
                            popup_shown = True
                        elif board.is_insufficient_material():
                            game_over = True
                            game_result = "insufficient"
                            popup_shown = True

                    dragger.stop_dragging()

            # Key press
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:  # Change theme
                    game.change_theme()
                elif event.key == pygame.K_r: # Resign
                    if not game_over:
                        game_over = True
                        game_result = "resignation"
                        popup_shown = True
                        board.game_result = "0-1" if game.state['current_player'] == 'white' else "1-0"

        # Display popup if game is over
        if game_over and popup_shown:
            winner = 'White' if game.state['current_player'] == 'black' else 'Black'
            show_result_popup(screen, game_result, winner)

        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()
import pygame
import socket
import select
from CONSTANT import *
from gameplaychess import ChessGame
from square import Square
from move import Move
from network import encode_move, encode_control, decode_message
from promotion import choose_promotion
from gameOver import show_result_popup

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("White Player")
    clock = pygame.time.Clock()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)
    conn, addr = server.accept()
    conn.setblocking(False)

    game = ChessGame(flipped=False)
    board = game.board
    dragger = game.dragger

    game_over = False
    popup_shown = False
    game_result = ""

    running = True
    while running:
        screen.fill((0, 0, 0))
        game.draw_board(screen)
        game.draw_last_move(screen)
        if not game_over:
            game.draw_valid_moves(screen)
        game.draw_pieces(screen)

        if dragger.state['is_dragging']:
            dragger.render(screen)

        # Receive message from client
        ready, _, _ = select.select([conn], [], [], 0)
        if ready:
            try:
                data = conn.recv(1024)
                if data:
                    msg = decode_message(data)
                    if msg['type'] == 'move' and not game_over:
                        sr, sc = msg['start']
                        er, ec = msg['end']
                        promotion = msg.get('promotion')
                        move = Move(Square(sr, sc), Square(er, ec))
                        move.promotion = promotion
                        piece = board.squares[sr][sc].piece
                        board.en_passant = tuple(msg['en_passant']) if msg['en_passant'] else None
                        board.move(piece, move, promotion_choice=promotion)
                        game.switch_turn()

                    elif msg['type'] == 'control':
                        action = msg['action']
                        if action in ['resign', 'game_over']:
                            game_over = True
                            popup_shown = True
                            game_result = msg['game_result']
                            board.game_result = "1-0" if msg.get('winner') == 'white' else "0-1"
                        elif action == 'restart':
                            game = ChessGame(flipped=False)
                            board = game.board
                            dragger = game.dragger
                            game_over = popup_shown = False
                            game_result = ""
                        elif action == 'theme_change':
                            game.change_theme()
            except:
                pass

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                board.save_pgn_to_file()
                running = False

            if game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        board.save_pgn_to_file()
                        game = ChessGame(flipped=False)
                        board = game.board
                        dragger = game.dragger
                        game_over = popup_shown = False
                        game_result = ""
                        conn.send(encode_control("restart"))
                    elif event.key == pygame.K_q:
                        board.save_pgn_to_file()
                        running = False
                continue

            if game.state['current_player'] == 'white':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.set_mouse_pos(event.pos)
                    row, col = dragger.state['mouse_y'] // SQUARE_SIZE, dragger.state['mouse_x'] // SQUARE_SIZE
                    if board.squares[row][col].has_piece():
                        piece = board.squares[row][col].piece
                        if piece.color == 'white':
                            board.calc_moves(piece, row, col, True)
                            dragger.set_start_square(event.pos)
                            dragger.start_dragging(piece)

                elif event.type == pygame.MOUSEMOTION:
                    if dragger.state['is_dragging']:
                        dragger.set_mouse_pos(event.pos)

                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.state['is_dragging']:
                        dragger.set_mouse_pos(event.pos)
                        sr, sc = dragger.state['start_row'], dragger.state['start_col']
                        er = dragger.state['mouse_y'] // SQUARE_SIZE
                        ec = dragger.state['mouse_x'] // SQUARE_SIZE
                        move = Move(Square(sr, sc), Square(er, ec))
                        piece = dragger.state['piece']

                        if board.valid_move(piece, move):
                            # Handle promotion if white
                            promotion_choice = None
                            if piece.name == 'pawn' and er == 7:
                                promotion_choice = choose_promotion(screen, piece.color)
                                move.promotion = promotion_choice
                            board.move(piece, move, promotion_choice=promotion_choice)
                            board.set_true_en_passant(piece)
                            conn.send(encode_move(move, board.en_passant))
                            game.switch_turn()

                            next_player = game.state['current_player']
                            if board.is_checkmate(next_player):
                                game_over = True
                                popup_shown = True
                                game_result = "checkmate"
                                board.game_result = "1-0"
                                conn.send(encode_control("game_over", winner="white", game_result="checkmate"))
                            elif board.is_stalemate(next_player):
                                game_over = True
                                popup_shown = True
                                game_result = "stalemate"
                                conn.send(encode_control("game_over", game_result="stalemate"))
                            elif board.is_threefold_repetition():
                                game_over = True
                                popup_shown = True
                                game_result = "repetition"
                                conn.send(encode_control("game_over", game_result="repetition"))
                            elif board.is_fifty_move_rule():
                                game_over = True
                                popup_shown = True
                                game_result = "50-move"
                                conn.send(encode_control("game_over", game_result="50-move"))
                            elif board.is_insufficient_material():
                                game_over = True
                                popup_shown = True
                                game_result = "insufficient"
                                conn.send(encode_control("game_over", game_result="insufficient"))

                    dragger.stop_dragging()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game_over = True
                        popup_shown = True
                        game_result = "resignation"
                        board.game_result = "0-1"
                        conn.send(encode_control("resign", winner="black", game_result="resignation"))
                    elif event.key == pygame.K_c:
                        game.change_theme()
                        conn.send(encode_control("theme_change"))

        if game_over and popup_shown:
            winner = 'White' if board.game_result == '1-0' else 'Black'
            show_result_popup(screen, game_result, winner)

        pygame.display.update()
        clock.tick(60)

    conn.close()
    server.close()
    pygame.quit()

if __name__ == '__main__':
    main()
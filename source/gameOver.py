import pygame
from CONSTANT import *

def show_result_popup(screen, result_type, winner=None):
    bg_color = BG_COLOR
    border_color = BORDER_COLOR
    text_color = TEXT_COLOR
    
    if result_type == "checkmate":
        title = f"{winner} won!"
        message = "Checkmate"
        bg_color = WIN_COLOR  
    elif result_type == "resignation":
        title = f"{winner} won!"
        message = "Resignation"
        bg_color = WIN_COLOR  
    elif result_type == "stalemate":
        title = "Game Drawn"
        message = "Stalemate"
        bg_color = DRAW_COLOR  
    elif result_type == "repetition":
        title = "Game Drawn"
        message = "Repetition"
        bg_color = DRAW_COLOR
    elif result_type == "50-move":
        title = "Game Drawn"
        message = "50-Move Rule"
        bg_color = DRAW_COLOR
    elif result_type == "insufficient":
        title = "Game Drawn"
        message = "Insufficient material"
        bg_color = DRAW_COLOR

    # Create fonts
    title_font = TITLE_FONT
    message_font = MSG_FONT
    hint_font = HINT_FONT

    # Create text surfaces
    title_text = title_font.render(title, True, text_color)
    message_text = message_font.render(message, True, text_color)
    hint_text = hint_font.render("Press N to restart or Q to quit", True, BORDER_COLOR)

    # Calculate popup dimensions
    popup_width = max(title_text.get_width(), message_text.get_width(), hint_text.get_width()) + 80
    popup_height = 180
    border_thickness = 4

    # Create rectangles
    screen_rect = screen.get_rect()
    border_rect = pygame.Rect(
        (screen_rect.width - popup_width) // 2 - border_thickness,
        (screen_rect.height - popup_height) // 2 - border_thickness,
        popup_width + border_thickness * 2,
        popup_height + border_thickness * 2
    )
    popup_rect = border_rect.inflate(-border_thickness * 2, -border_thickness * 2)

    # Draw the popup
    pygame.draw.rect(screen, border_color, border_rect, border_radius=10)
    pygame.draw.rect(screen, bg_color, popup_rect, border_radius=8)

    # Position and draw text
    title_pos = (popup_rect.centerx - title_text.get_width() // 2, popup_rect.top + 20)
    message_pos = (popup_rect.centerx - message_text.get_width() // 2, title_pos[1] + 50)
    hint_pos = (popup_rect.centerx - hint_text.get_width() // 2, popup_rect.bottom - 40)

    screen.blit(title_text, title_pos)
    screen.blit(message_text, message_pos)
    screen.blit(hint_text, hint_pos)

    # Update display
    pygame.display.update(border_rect)
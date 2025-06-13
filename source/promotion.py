import pygame
import os
from piece import Queen, Rook, Bishop, Knight
from CONSTANT import *

def choose_promotion(screen, color):
    clock = pygame.time.Clock()

    # Popup box position and size
    popup_rect = PROMOTION_BOX
    piece_rects = []
    piece_images = []

    # Load piece images and rects
    for i, name in enumerate(PIECE_OPTIONS):
        path = os.path.join('assets/images', f'{color}_{name}.png')
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (90, 90))
        rect = image.get_rect(topleft=(popup_rect.x + 5 + i * 75, popup_rect.y + 40))
        piece_images.append((image, rect))
        piece_rects.append(rect)

    # Draw the popup
    def draw_popup():
        pygame.draw.rect(screen, PROMOTION_COLOR, popup_rect)
        pygame.draw.rect(screen, PROMOTION_BORDER, popup_rect, 2)
        for image, rect in piece_images:
            screen.blit(image, rect)
        pygame.display.update()

    draw_popup()

    # Wait for user to click
    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(piece_rects):
                    if rect.collidepoint(event.pos):
                        return PIECE_OPTIONS[i]

def promote_to(piece_name, color):
    if piece_name == 'queen':
        return Queen(color)
    elif piece_name == 'rook':
        return Rook(color)
    elif piece_name == 'bishop':
        return Bishop(color)
    elif piece_name == 'knight':
        return Knight(color)
    return Queen(color)  
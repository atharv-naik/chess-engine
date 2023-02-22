import pygame
from board import Board
from pieces import Piece

clock = pygame.time.Clock()
FPS = 5

def main():
    board = Board()
    pressed_undo = False
    pressed_redo = False
    while board.play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                board.play = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                board.select(pygame.mouse.get_pos())
            elif event.type == pygame.KEYDOWN:
                mods = pygame.key.get_mods()
                if (mods & pygame.KMOD_CTRL) and (mods & pygame.KMOD_SHIFT) and event.key == pygame.K_z:  # ctrl + shift + z
                    pressed_redo = True
                    start = pygame.time.get_ticks()
                    board.redo()
                elif mods & pygame.KMOD_CTRL and event.key == pygame.K_z:  # ctrl + z
                    pressed_undo = True
                    start = pygame.time.get_ticks()
                    board.undo()
                elif mods & pygame.KMOD_CTRL and event.key == pygame.K_s:  # ctrl + s
                    board.save()
                elif mods & pygame.KMOD_CTRL and event.key == pygame.K_l:  # ctrl + l
                    board.load()
                elif event.key == pygame.K_s: # switch board color
                    board.switch_board_color()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_z:
                    if pressed_undo:
                        pressed_undo = False
                    elif pressed_redo:
                        pressed_redo = False
        if pressed_undo: # handle long press
            if pygame.time.get_ticks() - start >= board.LONG_PRESS_DELAY:
                board.undo()
        if pressed_redo: # handle long press
            if pygame.time.get_ticks() - start >= board.LONG_PRESS_DELAY:
                board.redo()
        board.draw(board.screen)
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
    pygame.quit()

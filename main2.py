import pygame
from board import Board
from pieces import Piece


def main():
    board = Board()
    while board.play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                board.play = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                board.select(pygame.mouse.get_pos())
            elif event.type == pygame.KEYDOWN:
                mods = pygame.key.get_mods()
                if (mods & pygame.KMOD_CTRL) and (mods & pygame.KMOD_SHIFT) and event.key == pygame.K_z:  # ctrl + shift + z
                    board.redo()
                elif mods & pygame.KMOD_CTRL and event.key == pygame.K_z:  # ctrl + z
                    board.undo()
                elif mods & pygame.KMOD_CTRL and event.key == pygame.K_s:  # ctrl + s
                    board.save()
                elif mods & pygame.KMOD_CTRL and event.key == pygame.K_l:  # ctrl + l
                    board.load()

        board.draw(board.screen)
        pygame.display.update()


if __name__ == "__main__":
    main()
    pygame.quit()

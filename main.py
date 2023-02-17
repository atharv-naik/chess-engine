import pygame
import backend
import copy
import json
from button import Button

DIMENSION = 800
HEIGHT = 1000
WIDTH = 800

WINDOW_SCALE = 0.9
DIMENSION = WINDOW_SCALE*DIMENSION
HEIGHT = WINDOW_SCALE*HEIGHT
WIDTH = WINDOW_SCALE*WIDTH

BRAWN_DARK = (255, 206, 158)
BRAWN_LIGHT = (209, 139, 71)

GREEN_DARK = (118, 150, 86)
GREEN_LIGHT = (238, 238, 210)

HIGHLIGHT_COLOR = (211, 107, 0)
HIGHLIGHT_COLOR = (104, 167, 173)
HIGHLIGHT_COLOR = (95, 111, 148)
HIGHLIGHT_COLOR = (186, 202, 68)

GREEN_BOARD = (GREEN_LIGHT, GREEN_DARK)  # light, dark

BROWN_BOARD = (BRAWN_LIGHT, BRAWN_DARK)  # light, dark


screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Chess")

# load assets
board = pygame.transform.scale(pygame.image.load(
    "assets/images/board.png"), (DIMENSION, DIMENSION))

bR = pygame.transform.scale(pygame.image.load(
    "assets/images/bR.png"), (DIMENSION // 8, DIMENSION // 8))
bN = pygame.transform.scale(pygame.image.load(
    "assets/images/bN.png"), (DIMENSION // 8, DIMENSION // 8))
bB = pygame.transform.scale(pygame.image.load(
    "assets/images/bB.png"), (DIMENSION // 8, DIMENSION // 8))
bQ = pygame.transform.scale(pygame.image.load(
    "assets/images/bQ.png"), (DIMENSION // 8, DIMENSION // 8))
bK = pygame.transform.scale(pygame.image.load(
    "assets/images/bK.png"), (DIMENSION // 8, DIMENSION // 8))
bP = pygame.transform.scale(pygame.image.load(
    "assets/images/bP.png"), (DIMENSION // 8, DIMENSION // 8))

wR = pygame.transform.scale(pygame.image.load(
    "assets/images/wR.png"), (DIMENSION // 8, DIMENSION // 8))
wN = pygame.transform.scale(pygame.image.load(
    "assets/images/wN.png"), (DIMENSION // 8, DIMENSION // 8))
wB = pygame.transform.scale(pygame.image.load(
    "assets/images/wB.png"), (DIMENSION // 8, DIMENSION // 8))
wQ = pygame.transform.scale(pygame.image.load(
    "assets/images/wQ.png"), (DIMENSION // 8, DIMENSION // 8))
wK = pygame.transform.scale(pygame.image.load(
    "assets/images/wK.png"), (DIMENSION // 8, DIMENSION // 8))
wP = pygame.transform.scale(pygame.image.load(
    "assets/images/wP.png"), (DIMENSION // 8, DIMENSION // 8))


start_img = pygame.image.load("assets/images/start_btn.png").convert_alpha()
exit_img = pygame.image.load("assets/images/exit_btn.png").convert_alpha()
start_img_width = start_img.get_width()
start_img_height = start_img.get_height()
exit_img_width = exit_img.get_width()
exit_img_height = exit_img.get_height()

start_button = Button(200*DIMENSION/800, HEIGHT/2 -
                      start_img_height/2, start_img, 0.7*DIMENSION/800)
exit_button = Button(WIDTH/2, HEIGHT/2 - exit_img_height /
                     2, exit_img, 0.7*DIMENSION/800)


def highlight_selection():
    if play:
        if sqselected is not None:
            a = sqselected[0]
            b = sqselected[1]+1
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, pygame.Rect(
                a * DIMENSION // 8, b * DIMENSION // 8, DIMENSION // 8, DIMENSION // 8))
    else:
        if sqselected is not None:
            a = sqselected[0]+1
            b = 0 if sqselected[1] == 0 else 9
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, pygame.Rect(
                a * DIMENSION // 8, b * DIMENSION // 8, DIMENSION // 8, DIMENSION // 8))


def draw_board(board):
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                pygame.draw.rect(screen, board[0], pygame.Rect(
                    i * DIMENSION // 8, (j+1) * DIMENSION // 8, DIMENSION // 8, DIMENSION // 8))
            else:
                pygame.draw.rect(screen, board[1], pygame.Rect(
                    i * DIMENSION // 8, (j+1) * DIMENSION // 8, DIMENSION // 8, DIMENSION // 8))


def draw_grid_border(color, thickness):
    for i in range(1, (WIDTH // (DIMENSION // 8))):
        pygame.draw.line(screen, color, (i * DIMENSION // 8, 100),
                         (i * DIMENSION // 8, HEIGHT - 100), thickness)
    for i in range(2, (HEIGHT // (DIMENSION // 8)) - 1):
        pygame.draw.line(screen, color, (0, i * DIMENSION // 8),
                         (WIDTH, i * DIMENSION // 8), thickness)


def draw_pool():
    for i in range(8):
        for j in range(8):
            if not play:
                if j == 0 and 1 <= i <= 6:
                    screen.blit(pool[0][i-1], (i * DIMENSION //
                                8, (0) * DIMENSION // 8))
                elif j == 7 and 1 <= i <= 6:
                    screen.blit(pool[1][i-1], (i * DIMENSION //
                                8, (9) * DIMENSION // 8))


def draw_pieces():
    for i in range(8):
        for j in range(8):
            if pieces[j][i] is not None:
                screen.blit(pieces[j][i], (i * DIMENSION //
                            8, (j+1) * DIMENSION // 8))


def draw_circle(i, j):
    pygame.draw.circle(screen, HIGHLIGHT_COLOR, (
        (i) * DIMENSION // 8 + DIMENSION // 16, (j) * DIMENSION // 8 + DIMENSION // 16), 0.1 * (DIMENSION // 8))


def show_valid_moves():
    if play:
        if sqselected is not None:
            a = sqselected[0]
            b = sqselected[1]
            if pieces[b][a] is not None:
                if pieces[b][a] == bK:
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if 0 <= a+i <= 7 and 0 <= b+j <= 7:
                                draw_circle(a+i, b+j+1)
                elif pieces[b][a] == bQ:
                    for i in range(-7, 8):
                        for j in range(-7, 8):
                            if 0 <= a+i <= 7 and 0 <= b+j <= 7 and (i == 0 or j == 0) and (i != 0 or j != 0):
                                draw_circle(a+i, b+j+1)
                            if 0 <= a+i <= 7 and 0 <= b+j <= 7 and (i != 0 or j != 0) and abs(i) == abs(j):
                                draw_circle(a+i, b+j+1)
                elif pieces[b][a] == bR:
                    for i in range(-7, 8):
                        for j in range(-7, 8):
                            if 0 <= a+i <= 7 and 0 <= b+j <= 7 and (i == 0 or j == 0) and (i != 0 or j != 0):
                                draw_circle(a+i, b+j+1)
                elif pieces[b][a] == bB:
                    for i in range(-7, 8):
                        for j in range(-7, 8):
                            if 0 <= a+i <= 7 and 0 <= b+j <= 7 and (i != 0 or j != 0) and abs(i) == abs(j):
                                draw_circle(a+i, b+j+1)
                elif pieces[b][a] == bN:
                    for i in (-2, -1, 1, 2):
                        for j in (-2, -1, 1, 2):
                            if 0 <= a+i <= 7 and 0 <= b+j <= 7 and (i != 0 or j != 0) and abs(i) != abs(j):
                                draw_circle(a+i, b+j+1)
                elif pieces[b][a] == bP:
                    if 0 <= b+1 <= 7:
                        draw_circle(a, b+2)
                elif pieces[b][a] == wK:
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if 0 <= a+i <= 7 and 0 <= b+j <= 7:
                                draw_circle(a+i, b+j+1)
                elif pieces[b][a] == wQ:
                    for i in range(-7, 8):
                        for j in range(-7, 8):
                            if 0 <= a+i <= 7 and 0 <= b+j <= 7 and (i == 0 or j == 0) and (i != 0 or j != 0):
                                draw_circle(a+i, b+j+1)
                            if 0 <= a+i <= 7 and 0 <= b+j <= 7 and (i != 0 or j != 0) and abs(i) == abs(j):
                                draw_circle(a+i, b+j+1)
                elif pieces[b][a] == wR:
                    for i in range(-7, 8):
                        for j in range(-7, 8):
                            if 0 <= a+i <= 7 and 0 <= b+j <= 7 and (i == 0 or j == 0) and (i != 0 or j != 0):
                                draw_circle(a+i, b+j+1)
                elif pieces[b][a] == wB:
                    for i in range(-7, 8):
                        for j in range(-7, 8):
                            if 0 <= a+i <= 7 and 0 <= b+j <= 7 and (i != 0 or j != 0) and abs(i) == abs(j):
                                draw_circle(a+i, b+j+1)
                elif pieces[b][a] == wN:
                    for i in (-2, -1, 1, 2):
                        for j in (-2, -1, 1, 2):
                            if 0 <= a+i <= 7 and 0 <= b+j <= 7 and (i != 0 or j != 0) and abs(i) != abs(j):
                                draw_circle(a+i, b+j+1)
                elif pieces[b][a] == wP:
                    if 0 <= b-1 <= 7:
                        draw_circle(a, b)


def update_pieces():
    piece_map = {
        "bK": bK, "bQ": bQ, "bR": bR, "bB": bB, "bN": bN, "bP": bP,
        "wK": wK, "wQ": wQ, "wR": wR, "wB": wB, "wN": wN, "wP": wP
    }
    for i in range(8):
        for j in range(8):
            pieces[j][i] = piece_map.get(piecesRep[j][i])



def update_piecesRep():
    piece_map = {
        bK: "bK", bQ: "bQ", bR: "bR", bB: "bB", bN: "bN", bP: "bP",
        wK: "wK", wQ: "wQ", wR: "wR", wB: "wB", wN: "wN", wP: "wP"
    }
    for i in range(8):
        for j in range(8):
            piecesRep[j][i] = piece_map.get(pieces[j][i])



def show_history():
    for i in range(8):
        for j in range(8):
            print(piecesRep[i][j], end="")
        print()
    print()


def check_undo_redo(event):
    global top, piecesRep, sqselected, play
    if play and event.type == pygame.KEYDOWN:
        mods = pygame.key.get_mods()
        # redo
        if (mods & pygame.KMOD_CTRL) and (mods & pygame.KMOD_SHIFT) and event.key == pygame.K_z:  # ctrl + shift + z
            if top < len(gamestate) - 1:
                top += 1
                piecesRep = copy.deepcopy(gamestate[top])
                sqselected = None
                # show_history()
                update_pieces()
        # undo
        elif mods & pygame.KMOD_CTRL and event.key == pygame.K_z:  # ctrl + z
            if top > 0:
                top -= 1
                piecesRep = copy.deepcopy(gamestate[top])
                sqselected = None
                # show_history()
                update_pieces()


def run_game_menu():
    global run_menu
    screen.fill((202, 228, 241))

    start_button.draw(screen)
    exit_button.draw(screen)

    if start_button.is_clicked():
        run_menu = False
    if exit_button.is_clicked():
        pygame.quit()
        quit()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    pygame.display.update()


def manage_save_load(event):
    global gamestate, top, piecesRep, loaded
    # save
    if play:
        if event.type == pygame.KEYDOWN:
            mods = pygame.key.get_mods()
            if mods & pygame.KMOD_CTRL and event.key == pygame.K_s:
                state = json.dumps([gamestate, top])
                with open("gamestate.json", "w") as f:
                    json.dump(state, f)
                print("saved")
    # load
    else:
        if event.type == pygame.KEYDOWN:
            mods = pygame.key.get_mods()
            if mods & pygame.KMOD_CTRL and event.key == pygame.K_l:
                try:
                    print("loading...", end="\r")
                    with open("gamestate.json", "r") as f:
                        state = json.load(f)
                    gamestate, top = json.loads(state)
                    gamestate = {int(k): v for k, v in gamestate.items()}
                    piecesRep = copy.deepcopy(gamestate[top])
                    update_pieces()
                    loaded = True
                    print("loaded successfully")
                except:
                    print("no save file found")


pieces = [[None] * 8 for _ in range(8)]  # empty board initialized
pool = [                        # pool of pieces to be placed on board
    [bK, bQ, bR, bB, bN, bP],
    [wK, wQ, wR, wB, wN, wP]
]

piecesRep = [[None] * 8 for _ in range(8)]

top = 0
play = False
run = True
sqselected = None
loaded = False
run_menu = True
while run:
    if run_menu:
        run_game_menu()
        continue

    # screen.fill(pygame.Color("white"))
    screen.fill((218, 208, 120))

    # blit changes on board

    # draw board
    draw_board(GREEN_BOARD)

    # highlight selection
    highlight_selection()
    show_valid_moves()
    # draw_grid_border(pygame.Color("black"), 1)

    # draw pool pieces
    draw_pool()

    # draw pieces
    draw_pieces()

    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # handling mouse events
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            y = int(pos[1] // (HEIGHT // 10))
            x = int(pos[0] // (WIDTH // 8))
            if not play:
                if sqselected is not None:
                    if 1 <= y <= 8:
                        pieces[y-1][x] = pool[sqselected[1]
                                              ][sqselected[0]]  # draw piece on board
                    else:
                        if y == 9:
                            y = 1
                        if sqselected == (x-1, y):
                            sqselected = None  # deselect piece
                        else:
                            sqselected = (x-1, y)  # select different piece
                elif y in (0, 9) and 1 <= x <= 6:
                    if y == 9:
                        y = 1
                    sqselected = (x-1, y)
            else:
                if 1 <= y <= 8:
                    if sqselected is not None:
                        if pieces[sqselected[1]][sqselected[0]] != pieces[y-1][x]:
                            pieces[sqselected[1]][sqselected[0]], pieces[y -
                                                                         1][x] = None, pieces[sqselected[1]][sqselected[0]]
                            piecesRep[sqselected[1]][sqselected[0]], piecesRep[y -
                                                                               1][x] = None, piecesRep[sqselected[1]][sqselected[0]]
                            top += 1
                            # show_history()
                            gamestate[top] = copy.deepcopy(piecesRep)
                            sqselected = None
                        else:
                            sqselected = None
                    else:
                        if pieces[y-1][x] is not None:
                            sqselected = (x, y-1)
                        else:
                            sqselected = None
                else:
                    sqselected = None

        # handling key presses
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:  # clear selection (c)
                sqselected = None

            if event.key == pygame.K_s and not play:  # start position (s)
                pieces = [
                    [bR, bN, bB, bQ, bK, bB, bN, bR],
                    [bP, bP, bP, bP, bP, bP, bP, bP],
                    [None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None],
                    [wP, wP, wP, wP, wP, wP, wP, wP],
                    [wR, wN, wB, wQ, wK, wB, wN, wR]
                ]
                sqselected = None

            if event.key == pygame.K_r and not play:  # reset board (r)
                pieces = [[None] * 8 for _ in range(8)]
                sqselected = None

            if event.key == pygame.K_k:  # play (k)
                play = not play
                sqselected = None
                if play:
                    update_piecesRep()
                    if not loaded:
                        gamestate = {0: copy.deepcopy(piecesRep)}

        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            screen.fill((218, 208, 120))
            draw_board(GREEN_BOARD)
            draw_pool()
            draw_pieces()

        # undo and redo
        check_undo_redo(event)

        # save and load
        manage_save_load(event)

    pygame.display.update()

pygame.quit()
quit()

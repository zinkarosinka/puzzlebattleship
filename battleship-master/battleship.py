#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is a project powered by Codecademy students.
The project features a modified single-player version of the classic game: battleships.

Game based on tutorials by Al Sweigart in his book 'Making Games with Python
& Pygame"
http://inventwithpython.com/pygame/chapters/

The game requires python 2 and the pygame modules.
The game is a battleship puzzle game. The objective is to sink all the ships in as few shots as possible.
The markers on the edges of the game board tell you how many ship pieces are in each column and row.
"""
# Importing pygame modules
import random, sys, pygame
from pygame.locals import *

# Set variables, like screen width and height 
# globals
FPS = 30 #Determines the number of frames per second
REVEALSPEED = 8 #Determines the speed at which the squares reveals after being clicked
WINDOWWIDTH = 800 #Width of game window
WINDOWHEIGHT = 600 #Height of game window
TILESIZE = 40 #Size of the squares in each grid(tile)
MARKERSIZE = 40 #Size of the box which contatins the number that indicates how many ships in this row/col
BUTTONHEIGHT = 20 #Height of a standard button
BUTTONWIDTH = 40 #Width of a standard button
TEXT_HEIGHT = 25 #Size of the text
TEXT_LEFT_POSN = 10 #Where the text will be positioned
BOARDWIDTH = 10 #Number of grids horizontally
BOARDHEIGHT = 10 #Number of grids vertically
DISPLAYWIDTH = 200 #Width of the game board
EXPLOSIONSPEED = 10 #How fast the explosion graphics will play

XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * TILESIZE) - DISPLAYWIDTH - MARKERSIZE) / 2) #x-position of the top left corner of board 
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * TILESIZE) - MARKERSIZE) / 2) #y-position of the top left corner of board

#Colours which will be used by the game
BLACK   = (  0,   0,   0)
WHITE   = (255, 255, 255)
GREEN   = (  0, 204,   0)
GRAY    = ( 60,  60,  60)
BLUE    = (  0,  50, 255)
YELLOW  = (255, 255,   0)
DARKGRAY =( 40,  40,  40)

#Determine what to colour each element of the game
BGCOLOR = GRAY
BUTTONCOLOR = GREEN
TEXTCOLOR = WHITE
TILECOLOR = GREEN
BORDERCOLOR = BLUE
TEXTSHADOWCOLOR = BLUE
SHIPCOLOR = YELLOW
HIGHLIGHTCOLOR = BLUE


def main():
    """
    The main function intializes the variables which will be used by the game.
    """
    global DISPLAYSURF, FPSCLOCK, BASICFONT, HELP_SURF, HELP_RECT, NEW_SURF, \
           NEW_RECT, SHOTS_SURF, SHOTS_RECT, BIGFONT, COUNTER_SURF, \
           COUNTER_RECT, HBUTTON_SURF, EXPLOSION_IMAGES
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    #Fonts used by the game
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 20)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 50)
    
    # Create and label the buttons
    HELP_SURF = BASICFONT.render("HELP", True, WHITE)
    HELP_RECT = HELP_SURF.get_rect()
    HELP_RECT.topleft = (WINDOWWIDTH - 180, WINDOWHEIGHT - 350)
    NEW_SURF = BASICFONT.render("NEW GAME", True, WHITE)
    NEW_RECT = NEW_SURF.get_rect()
    NEW_RECT.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 200)

    # The 'Shots:' label at the top
    SHOTS_SURF = BASICFONT.render("Shots: ", True, WHITE)
    SHOTS_RECT = SHOTS_SURF.get_rect()
    SHOTS_RECT.topleft = (WINDOWWIDTH - 750, WINDOWHEIGHT - 570)
    
    # Load the explosion graphics from the /img folder
    EXPLOSION_IMAGES = [
        pygame.image.load("img/blowup1.png"), pygame.image.load("img/blowup2.png"),
        pygame.image.load("img/blowup3.png"),pygame.image.load("img/blowup4.png"),
        pygame.image.load("img/blowup5.png"),pygame.image.load("img/blowup6.png")]
    
    # Set the title in the menu bar to 'Battleship'
    pygame.display.set_caption('Battleship')

    # Keep the game running at all times
    while True:
        shots_taken = run_game() #Run the game until it stops and save the result in shots_taken
        show_gameover_screen(shots_taken) #Display a gameover screen by passing in shots_taken
        
        
def run_game():
    """
    Function is executed while a game is running.
    
    returns the amount of shots taken
    """
    revealed_tiles = generate_default_tiles(False) #Contains the list of the tiles revealed by user
    # main board object, 
    main_board = generate_default_tiles(None) #Contains the list of the ships which exists on board
    ship_objs = ['battleship','cruiser1','cruiser2','destroyer1','destroyer2',
                 'destroyer3','submarine1','submarine2','submarine3','submarine4'] # List of the ships available
    main_board = add_ships_to_board(main_board, ship_objs) #call add_ships_to_board to add the list of ships to the main_board
    mousex, mousey = 0, 0 #location of mouse
    counter = [] #counter to track number of shots fired
    xmarkers, ymarkers = set_markers(main_board) #The numerical markers on each side of the board
        
    while True:
        # counter display (it needs to be here in order to refresh it)
        COUNTER_SURF = BASICFONT.render(str(len(counter)), True, WHITE)
        COUNTER_RECT = SHOTS_SURF.get_rect()
        COUNTER_RECT.topleft = (WINDOWWIDTH - 680, WINDOWHEIGHT - 570)
        
        # Fill background
        DISPLAYSURF.fill(BGCOLOR)
        
        # draw the buttons
        DISPLAYSURF.blit(HELP_SURF, HELP_RECT)
        DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
        DISPLAYSURF.blit(SHOTS_SURF, SHOTS_RECT)
        DISPLAYSURF.blit(COUNTER_SURF, COUNTER_RECT)
        
        # Draw the tiles onto the board and their respective markers
        draw_board(main_board, revealed_tiles)
        draw_markers(xmarkers, ymarkers)
        
        mouse_clicked = False

        check_for_quit()
        #Check for pygame events
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                if HELP_RECT.collidepoint(event.pos): #if the help button is clicked on 
                    DISPLAYSURF.fill(BGCOLOR)
                    show_help_screen() #Show the help screen
                elif NEW_RECT.collidepoint(event.pos): #if the new game button is clicked on
                    main() #goto main, which resets the game
                else: #otherwise
                    mousex, mousey = event.pos #set mouse positions to the new position
                    mouse_clicked = True #mouse is clicked but not on a button
            elif event.type == MOUSEMOTION: #Detected mouse motion
                mousex, mousey = event.pos #set mouse positions to the new position
        
        #Check if the mouse is clicked at a position with a ship piece
        tilex, tiley = get_tile_at_pixel(mousex, mousey) 
        if tilex != None and tiley != None:
            if not revealed_tiles[tilex][tiley]: #if the tile the mouse is on is not revealed
                draw_highlight_tile(tilex, tiley) # draws the hovering highlight over the tile
            if not revealed_tiles[tilex][tiley] and mouse_clicked: #if the mouse is clicked on the not revealed tile
                reveal_tile_animation(main_board, [(tilex, tiley)])
                revealed_tiles[tilex][tiley] = True #set the tile to now be revealed
                if check_revealed_tile(main_board, [(tilex, tiley)]): # if the clicked position contains a ship piece
                    left, top = left_top_coords_tile(tilex, tiley)
                    blowup_animation((left, top)) 
                    if check_for_win(main_board, revealed_tiles): # check for a win
                        counter.append((tilex, tiley))
                        return len(counter) # return the amount of shots taken
                counter.append((tilex, tiley))
                
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generate_default_tiles(default_value):
    """
    Function generates a list of 10 x 10 tiles. The list will contain tuples
    ('shipName', boolShot) set to their (default_value).
    
    default_value -> boolean which tells what the value to set to
    the list of tuples
    """
    default_tiles = [[default_value]*BOARDHEIGHT for i in range(BOARDWIDTH)]
    
    return default_tiles

    
def blowup_animation(coord):
    """
    Function creates the explosition played if a ship is shot.
    
    coord -> tuple of tile coords to apply the blowup animation
    """
    for image in EXPLOSION_IMAGES: # go through the list of images in the list of pictures and play them in sequence 
        #Determine the location and size to display the image
        image = pygame.transform.scale(image, (TILESIZE+10, TILESIZE+10))
        DISPLAYSURF.blit(image, coord)
        pygame.display.flip()
        FPSCLOCK.tick(EXPLOSIONSPEED) #Determine the delay to play the image with


def check_revealed_tile(board, tile):
    """
    Function checks if a tile location contains a ship piece.
    
    board -> the tiled board either a ship piece or none
    tile -> location of tile
    returns True if ship piece exists at tile location
    """
    return board[tile[0][0]][tile[0][1]] != None


def reveal_tile_animation(board, tile_to_reveal):
    """
    Function creates an animation which plays when the mouse is clicked on a tile, and whatever is
    behind the tile needs to be revealed.
    
    board -> list of board tile tuples ('shipName', boolShot)
    tile_to_reveal -> tuple of tile coords to apply the reveal animation to
    """
    for coverage in range(TILESIZE, (-REVEALSPEED) - 1, -REVEALSPEED): #Plays animation based on reveal speed
        draw_tile_covers(board, tile_to_reveal, coverage)

        
def draw_tile_covers(board, tile, coverage):
    """
    Function draws the tiles according to a set of variables.
    
    board -> list; of board tiles
    tile -> tuple; of tile coords to reveal
    coverage -> int; amount of the tile that is covered
    """
    left, top = left_top_coords_tile(tile[0][0], tile[0][1])
    if check_revealed_tile(board, tile):
        pygame.draw.rect(DISPLAYSURF, SHIPCOLOR, (left, top, TILESIZE,
                                                  TILESIZE))
    else:
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, TILESIZE,
                                                TILESIZE))
    if coverage > 0:
        pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left, top, coverage,
                                                  TILESIZE))
            
    pygame.display.update()
    FPSCLOCK.tick(FPS)    


def check_for_quit():
    """
    Function checks if the user has attempted to quit the game.
    """
    for event in pygame.event.get(QUIT):
        pygame.quit()
        sys.exit()


def check_for_win(board, revealed):
    """
    Function checks if the current board state is a winning state.
    
    board -> the board which contains the ship pieces
    revealed -> list of revealed tiles
    returns True if all the ships are revealed
    """
    for tilex in range(BOARDWIDTH):
        for tiley in range(BOARDHEIGHT):
            if board[tilex][tiley] != None and not revealed[tilex][tiley]: # check if every board with a ship is revealed, return false if not
                return False
    return True


def draw_board(board, revealed):
    """
    Function draws the game board.
    
    board -> list of board tiles
    revealed -> list of revealed tiles
    """
    #draws the grids depending on its state
    for tilex in range(BOARDWIDTH):
        for tiley in range(BOARDHEIGHT):
            left, top = left_top_coords_tile(tilex, tiley)
            if not revealed[tilex][tiley]:
                pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left, top, TILESIZE,
                                                          TILESIZE))
            else:
                if board[tilex][tiley] != None:
                    pygame.draw.rect(DISPLAYSURF, SHIPCOLOR, (left, top, 
                                     TILESIZE, TILESIZE))
                else:
                    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, 
                                     TILESIZE, TILESIZE))
    #draws the horizontal lines            
    for x in range(0, (BOARDWIDTH + 1) * TILESIZE, TILESIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x + XMARGIN + MARKERSIZE,
            YMARGIN + MARKERSIZE), (x + XMARGIN + MARKERSIZE, 
            WINDOWHEIGHT - YMARGIN))
    #draws the vertical lines
    for y in range(0, (BOARDHEIGHT + 1) * TILESIZE, TILESIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (XMARGIN + MARKERSIZE, y + 
            YMARGIN + MARKERSIZE), (WINDOWWIDTH - (DISPLAYWIDTH + MARKERSIZE *
            2), y + YMARGIN + MARKERSIZE))

        
def set_markers(board):
    """
    Function creates the lists of the markers to the side of the game board which indicates
    the number of ship pieces in each row and column.
    
    board: list of board tiles
    returns the 2 lists of markers with number of ship pieces in each row (xmarkers)
        and column (ymarkers)
    """
    xmarkers = [0 for i in range(BOARDWIDTH)]
    ymarkers = [0 for i in range(BOARDHEIGHT)]
    #Loop through the tiles
    for tilex in range(BOARDWIDTH):
        for tiley in range(BOARDHEIGHT):
            if board[tilex][tiley] != None: #if the tile is a ship piece, then increment the markers 
                xmarkers[tilex] += 1
                ymarkers[tiley] += 1

    return xmarkers, ymarkers


def draw_markers(xlist, ylist):
    """
    Function draws the two list of markers to the side of the board.

    xlist -> list of row markers
    ylist -> list of column markers
    """
    for i in range(len(xlist)): #Draw the x-marker list
        left = i * MARKERSIZE + XMARGIN + MARKERSIZE + (TILESIZE / 3)
        top = YMARGIN
        marker_surf, marker_rect = make_text_objs(str(xlist[i]),
                                                    BASICFONT, TEXTCOLOR)
        marker_rect.topleft = (left, top)
        DISPLAYSURF.blit(marker_surf, marker_rect)
    for i in range(len(ylist)): #Draw the y-marker list
        left = XMARGIN
        top = i * MARKERSIZE + YMARGIN + MARKERSIZE + (TILESIZE / 3)
        marker_surf, marker_rect = make_text_objs(str(ylist[i]), 
                                                    BASICFONT, TEXTCOLOR)
        marker_rect.topleft = (left, top)
        DISPLAYSURF.blit(marker_surf, marker_rect)



def add_ships_to_board(board, ships):
    """
    Function goes through a list of ships and add them randomly into a board.
    
    board -> list of board tiles
    ships -> list of ships to place on board
    returns list of board tiles with ships placed on certain tiles
    """
    new_board = board[:]
    ship_length = 0
    for ship in ships: #go through each ship declared in the list
        #Randomly find a valid position that fits the ship
        valid_ship_position = False
        while not valid_ship_position:
            xStartpos = random.randint(0, 9)
            yStartpos = random.randint(0, 9)
            isHorizontal = random.randint(0, 1) #vertical or horizontal positioning
            #Type of ship and their respective length
            if 'battleship' in ship:
                ship_length = 4
            elif 'cruiser' in ship:
                ship_length = 3
            elif 'destroyer'in ship:
                ship_length = 2
            elif 'submarine' in ship:
                ship_length = 1
            
            #check if position is valid
            valid_ship_position, ship_coords = make_ship_position(new_board,
                xStartpos, yStartpos, isHorizontal, ship_length, ship)
            #add the ship if it is valid
            if valid_ship_position:
                for coord in ship_coords:
                    new_board[coord[0]][coord[1]] = ship
    return new_board


def make_ship_position(board, xPos, yPos, isHorizontal, length, ship):
    """
    Function makes a ship on a board given a set of variables
    
    board -> list of board tiles
    xPos -> x-coordinate of first ship piece
    yPos -> y-coordinate of first ship piece
    isHorizontal -> True if ship is horizontal
    length -> length of ship
    returns tuple: True if ship position is valid and list ship coordinates
    """
    ship_coordinates = [] #the coordinates the ship will occupy
    if isHorizontal:
        for i in range(length):
            if (i+xPos > 9) or (board[i+xPos][yPos] != None) or \
                hasAdjacent(board, i+xPos, yPos, ship): #if the ship goes out of bound, hits another ship, or is adjacent to another ship
                return (False, ship_coordinates) #then return false
            else:
                ship_coordinates.append((i+xPos, yPos))
    else:
        for i in range(length):
            if (i+yPos > 9) or (board[xPos][i+yPos] != None) or \
                hasAdjacent(board, xPos, i+yPos, ship): #if the ship goes out of bound, hits another ship, or is adjacent to another ship
                return (False, ship_coordinates) #then return false        
            else:
                ship_coordinates.append((xPos, i+yPos))
    return (True, ship_coordinates) #ship is successfully added


def hasAdjacent(board, xPos, yPos, ship):
    """
    Funtion checks if a ship has adjacent ships
    
    board -> list of board tiles
    xPos -> x-coordinate of first ship piece
    yPos -> y-coordinate of first ship piece
    ship -> the ship being checked for adjacency
    returns true if there are adjacent ships and false if there are no adjacent ships
    """
    for x in range(xPos-1,xPos+2):
        for y in range(yPos-1,yPos+2):
            if (x in range (10)) and (y in range (10)) and \
                (board[x][y] not in (ship, None)):
                return True
    return False
    
    
def left_top_coords_tile(tilex, tiley):
    """
    Function calculates and returns the pixel of the tile in the top left corner
    
    tilex -> int; x position of tile
    tiley -> int; y position of tile
    returns tuple (int, int) which indicates top-left pixel coordinates of tile
    """
    left = tilex * TILESIZE + XMARGIN + MARKERSIZE
    top = tiley * TILESIZE + YMARGIN + MARKERSIZE
    return (left, top)
    
    
def get_tile_at_pixel(x, y):
    """
    Function finds the corresponding tile coordinates of pixel at top left, defaults to (None, None) given a coordinate.
    
    x -> int; x position of pixel
    y -> int; y position of pixel
    returns tuple (tilex, tiley) 
    """
    for tilex in range(BOARDWIDTH):
        for tiley in range(BOARDHEIGHT):
            left, top = left_top_coords_tile(tilex, tiley)
            tile_rect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tile_rect.collidepoint(x, y):
                return (tilex, tiley)
    return (None, None)
    
    
def draw_highlight_tile(tilex, tiley):
    """
    Function draws the hovering highlight over the tile.
    
    tilex -> int; x position of tile
    tiley -> int; y position of tile
    """
    left, top = left_top_coords_tile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR,
                    (left, top, TILESIZE, TILESIZE), 4)


def show_help_screen():
    """
    Function display a help screen until any button is pressed.
    """
    line1_surf, line1_rect = make_text_objs('Press a key to return to the game', 
                                            BASICFONT, TEXTCOLOR)
    line1_rect.topleft = (TEXT_LEFT_POSN, TEXT_HEIGHT)
    DISPLAYSURF.blit(line1_surf, line1_rect)
    
    line2_surf, line2_rect = make_text_objs(
        'This is a battleship puzzle game. Your objective is ' \
        'to sink all the ships in as few', BASICFONT, TEXTCOLOR)
    line2_rect.topleft = (TEXT_LEFT_POSN, TEXT_HEIGHT * 3)
    DISPLAYSURF.blit(line2_surf, line2_rect)

    line3_surf, line3_rect = make_text_objs('shots as possible. The markers on'\
        ' the edges of the game board tell you how', BASICFONT, TEXTCOLOR)
    line3_rect.topleft = (TEXT_LEFT_POSN, TEXT_HEIGHT * 4)
    DISPLAYSURF.blit(line3_surf, line3_rect)

    line4_surf, line4_rect = make_text_objs('many ship pieces are in each'\
        ' column and row. To reset your game click on', BASICFONT, TEXTCOLOR)
    line4_rect.topleft = (TEXT_LEFT_POSN, TEXT_HEIGHT * 5)
    DISPLAYSURF.blit(line4_surf, line4_rect)

    line5_surf, line5_rect = make_text_objs('the "New Game" button.',
        BASICFONT, TEXTCOLOR)
    line5_rect.topleft = (TEXT_LEFT_POSN, TEXT_HEIGHT * 6)
    DISPLAYSURF.blit(line5_surf, line5_rect)
    
    while check_for_keypress() == None: #Check if the user has pressed keys, if so go back to the game
        pygame.display.update()
        FPSCLOCK.tick()

        
def check_for_keypress():
    """
    Function checks for any key presses by pulling out all KEYDOWN and KEYUP events from queue.
    
    returns any KEYUP events, otherwise return None
    """
    for event in pygame.event.get([KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION]):
        if event.type in (KEYDOWN, MOUSEBUTTONUP, MOUSEBUTTONDOWN, MOUSEMOTION):
            continue
        return event.key
    return None

    
def make_text_objs(text, font, color):
    """
    Function creates a text.
    
    text -> string; content of text
    font -> Font object; face of font
    color -> tuple of color (red, green blue); colour of text
    returns the surface object, rectangle object
    """
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def show_gameover_screen(shots_fired):
    """
    Function display a gameover screen when the user has successfully shot at every ship pieces.
    
    shots_fired -> the number of shots taken before game is over
    """
    DISPLAYSURF.fill(BGCOLOR)
    titleSurf, titleRect = make_text_objs('Congrats! Puzzle solved in:',
                                            BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(titleSurf, titleRect)
    
    titleSurf, titleRect = make_text_objs('Congrats! Puzzle solved in:', 
                                            BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)
    
    titleSurf, titleRect = make_text_objs(str(shots_fired) + ' shots', 
                                            BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2 + 50))
    DISPLAYSURF.blit(titleSurf, titleRect)
    
    titleSurf, titleRect = make_text_objs(str(shots_fired) + ' shots', 
                                            BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2 + 50) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)

    pressKeySurf, pressKeyRect = make_text_objs(
        'Press a key to try to beat that score.', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)
    
    while check_for_keypress() == None: #Check if the user has pressed keys, if so start a new game
        pygame.display.update()
        FPSCLOCK.tick()    
        
    
if __name__ == "__main__": #This calls the game loop
    main()

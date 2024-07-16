import pygame
import random 
import sys


#Initialize pygame
pygame.init()
pygame.font.init()

#Global variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
FPS = 10
WIDTH, HEIGHT = 7, 6
RED_SCORE = 0
YELLOW_SCORE = 0

#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

YELLOW_WON = pygame.USEREVENT + 1
RED_WON = pygame.USEREVENT + 2


#Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Four in a row")


FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 60)

def get_pos():
    pos = pygame.mouse.get_pos()
    return pos

def get_rect(grid, pos):
    for rect in grid:
        try:
            if rect.collidepoint(pos):
                return rect
        except:
            rect_x = rect[0]
            rect_y = rect[1]
            if rect_x < pos[0] < rect_x + 50 and rect_y < pos[1] < rect_y + 50:
                return rect  
    return None

def check_winner(chips):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            current = chips[y][x]
            if current == 0:
                continue
                
            #Creating a 3x3 grid over chip[x][y]
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue            
                    counter = 1
                    for n in range(1, 4):
                        new_x = x + j * n
                        new_y = y + i * n
                
                        #Checking if new coordinate is out of bounds
                        if  new_x < 0 or new_x >= WIDTH:
                            continue
                        if new_y < 0 or new_y >= HEIGHT:
                            continue  
                        if chips[new_y][new_x] == current:
                            counter += 1
                        else:
                            break

                    #Checking if we have a winner
                    if counter >= 4:
                        if current == 1:
                            pygame.event.post(pygame.event.Event(YELLOW_WON))
                            return current
                        if current == 2:
                            pygame.event.post(pygame.event.Event(RED_WON))
                            return current
                        

def draw_window(red_circles, yellow_circles, grid, pos, turn_display, turn, winner):
    pygame.draw.rect(screen, WHITE, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    
    #Drawing the turn display
    
    text = FONT.render("Turn: ", 1, BLACK)
    screen.blit(text, (450, 100))
    if (turn % 2 == 0):
        pygame.draw.rect(screen, YELLOW, turn_display)
    else:
        pygame.draw.rect(screen, RED, turn_display)
        
    #Drawing grid
    for rect in grid:
        pygame.draw.rect(screen, WHITE, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)
    
    #Drawing circles
    for circle in red_circles:
                pygame.draw.circle(screen, RED, circle, 20, 20)
    for circle in yellow_circles:
                pygame.draw.circle(screen, YELLOW, circle, 20, 20)
    
    #Drawing the winner
    if winner == 1:
        winner_text = WINNER_FONT.render("Yellow Won!", 1, YELLOW)
        screen.blit(winner_text, (450, 200))
    if winner == 2:
        winner_text = WINNER_FONT.render("Red Won!", 1, RED)
        screen.blit(winner_text, (450, 200))
    
    #Drawing the scoreboard
    red_text = "Red: " + str(RED_SCORE)
    red_score = FONT.render(red_text, 1, BLACK)
    yellow_text = "Yellow: " + str(YELLOW_SCORE)
    yellow_score = FONT.render(yellow_text, 1, BLACK)
    
    screen.blit(red_score, (450, 10))
    screen.blit(yellow_score, (600, 10))
    
    #Highlighting the column
    rect = get_rect(grid, pos)
    if rect:
        highlight = pygame.Surface((rect.width, 300), pygame.SRCALPHA)
        highlight.fill((0, 0, 255, 100))  # White with transparency
        screen.blit(highlight, (rect.x, 50))

    pygame.display.update()

def main():
    global YELLOW_SCORE, RED_SCORE
    
    run = True
    red_circles = []
    yellow_circles = []
    clock = pygame.time.Clock()

    chips = [[0 for i in range(WIDTH)] for j in range(HEIGHT)]
    grid = []
    turn = 0
    turn_display = pygame.Rect(580, 110, 50, 50)
    winner = 0
    
    for i in range(HEIGHT):
        for j in range(WIDTH):
            rect = pygame.Rect(50 + 50*j, 50 + 50*i, 50, 50)
            grid.append(rect)

            
    
    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == YELLOW_WON:
                winner = 1
                YELLOW_SCORE += 1
            if event.type == RED_WON:
                winner = 2
                RED_SCORE += 1
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Adding chips to the botton of the row
                rect = get_rect(grid, get_pos())
                if rect:
                    column = rect.x//50 - 1
                    for row in range(HEIGHT - 1, -1, -1):  # Start from bottom row
                        if chips[row][column] == 0:
                            if turn % 2 == 0:
                                turn += 1
                                yellow_circles.append((rect.x + 25, 50 + 25 + 50 * row))
                                chips[row][column] = 1
                            else:
                                turn += 1
                                red_circles.append((rect.x + 25, 50 + 25 + 50 * row))
                                chips[row][column] = 2
                            break
                check_winner(chips)
        
        
        pos = get_pos()
        
        draw_window(red_circles, yellow_circles, grid, pos, turn_display, turn, winner)
        
        if winner != 0:
            pygame.time.delay(4000)
            main()

    pygame.quit()
    
if __name__ == "__main__":
    main()
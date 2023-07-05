import pygame
from pathfinding import astar, dijkstras, bfs, bidirectional
from constants import *

# draw methods
def draw_text(main_menu):
    font = pygame.font.Font('assets/font.ttf', 50)
    text = font.render('Pathfinding Visualizer', False, WHITE)
    main_menu.blit(text, (WIDTH // 2 - text.get_width()//2+2, 30+6))
    text = font.render('Pathfinding Vizualizer', False, BLACK)
    main_menu.blit(text, (WIDTH // 2 - text.get_width()//2, 30))
    text = font.render('Select an algorithm:', False, WHITE)
    main_menu.blit(text, (WIDTH // 2 - text.get_width()//2+2, 110+6))
    text = font.render('Select an algorithm:', False, BLACK)
    main_menu.blit(text, (WIDTH // 2 - text.get_width()//2, 110))
    
def draw_buttons(main_menu):
    button1 = pygame.Rect(B_X1, B_Y1, B_WIDTH, B_HEIGHT)
    button2 = pygame.Rect(B_X2, B_Y2, B_WIDTH, B_HEIGHT)
    button3 = pygame.Rect(B_X3, B_Y3, B_WIDTH, B_HEIGHT)
    button4 = pygame.Rect(B_X4, B_Y4, B_WIDTH, B_HEIGHT)
    font = pygame.font.Font('assets/font.ttf', 25)
    # button 1
    pygame.draw.rect(main_menu, BLACK, button1.move(2, 6), border_radius=12)
    pygame.draw.rect(main_menu, DARK_GREY, button1, border_radius=12)
    text = font.render('A *', False, WHITE)
    main_menu.blit(text, (button1.center[0]-text.get_width()//2+1, button1.center[1]-text.get_height()//2+2))
    text = font.render('A *', False, BLACK)
    main_menu.blit(text, (button1.center[0]-text.get_width()//2, button1.center[1]-text.get_height()//2))
    # button 2
    pygame.draw.rect(main_menu, BLACK, button2.move(2, 6), border_radius=12)
    pygame.draw.rect(main_menu, DARK_GREY, button2, border_radius=12)
    text = font.render('Dijkstra\'s', False, WHITE)
    main_menu.blit(text, (button2.center[0]-text.get_width()//2+1, button2.center[1]-text.get_height()//2+2))
    text = font.render('Dijkstra\'s', False, BLACK)
    main_menu.blit(text, (button2.center[0]-text.get_width()//2, button2.center[1]-text.get_height()//2))
    # button 3
    pygame.draw.rect(main_menu, BLACK, button3.move(2, 6), border_radius=12)
    pygame.draw.rect(main_menu, DARK_GREY, button3, border_radius=12)
    text = font.render('Bidirectional', False, WHITE)
    main_menu.blit(text, (button3.center[0]-text.get_width()//2+1, button3.center[1]-text.get_height()//2+2))
    text = font.render('Bidirectional', False, BLACK)
    main_menu.blit(text, (button3.center[0]-text.get_width()//2, button3.center[1]-text.get_height()//2))
    # button 4
    pygame.draw.rect(main_menu, BLACK, button4.move(2, 6), border_radius=12)
    pygame.draw.rect(main_menu, DARK_GREY, button4, border_radius=12)
    text = font.render('BFS', False, WHITE)
    main_menu.blit(text, (button4.center[0]-text.get_width()//2+1, button4.center[1]-text.get_height()//2+2))
    text = font.render('BFS', False, BLACK)
    main_menu.blit(text, (button4.center[0]-text.get_width()//2, button4.center[1]-text.get_height()//2))

def draw_instructions(main_menu):
    font = pygame.font.Font('assets/font.ttf', 30)
    instructions = "Press Space to run\nPress c to clear screen\nLeft click to add nodes\nRight click to remove nodes\nPress esc to return to main menu"
    ins = instructions.split("\n")
    for i in range(len(ins)):
        text = font.render(ins[i], False, BLACK)
        main_menu.blit(text, (WIDTH/2-text.get_width()//2, 500+i*40))

def main():
    pygame.init()   # initialize all imported pygame modules
    main_menu = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption('Path finder')
    icon = pygame.image.load('assets/icon.png')
    pygame.display.set_icon(icon)

    running = True
    while running == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.MOUSEBUTTONUP:
                (x, y) = pygame.mouse.get_pos()
                if B_X1 < x < B_X1 + B_WIDTH and B_Y1 < y < B_Y1 + B_HEIGHT:
                    astar(main_menu, WIDTH)
                elif B_X2 < x < B_X2 + B_WIDTH and B_Y2 < y < B_Y2 + B_HEIGHT:
                    dijkstras(main_menu, WIDTH)
                elif B_X3 < x < B_X3 + B_WIDTH and B_Y3 < y < B_Y3 + B_HEIGHT:
                    bidirectional(main_menu, WIDTH)
                elif B_X4 < x < B_X4 + B_WIDTH and B_Y4 < y < B_Y4 + B_HEIGHT:
                    bfs(main_menu, WIDTH)

        main_menu.fill(GREY)
        # display text
        draw_text(main_menu)
        # draw buttons
        draw_buttons(main_menu)
        # instructions
        draw_instructions(main_menu)
        pygame.display.update()







if __name__ == '__main__':
    main()
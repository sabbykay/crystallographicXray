import pygame 
from pygame.locals import *
from clifford import Cl

pygame.init()
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Diffractometer Angle Button Controls") #Set the window title

scene = Cl(3)
angles = [0, 0, 0]

#Define button positions and dimenstions
button_width = 200
button_height = 50
button_padding = 20

button_positions = [
    (button_padding, height // 2 - button_height - button_padding),
    (button_padding, height // 2),
    (button_padding, height // 2 + button_height + button_padding)]

button_color = (100, 100, 100)
button_hover_color = (150, 150, 150)


def increment_angle(index):
    angles[index] += 0.1

def check_button_click(mouse_pos, index):
    button_x, button_y = button_positions[index]
    return button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height


running = True
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                for i in range(len(button_positions)):
                    if check_button_click(mouse_pos, i):
                        increment_angle(i)
    
    window.fill((255, 255, 255))

    #Render the buttons
    for i, position in enumerate(button_positions):
        button_x, button_y = position
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        button_color_to_use = button_hover_color if check_button_click(pygame.mouse.get_pos(), i) else button_color
        pygame.draw.rect(window, button_color_to_use, button_rect)
        #Render button text
        font = pygame.font.Font(None, 30)
        button_text = font.render(f"Angle {i+1}: {angles[i]:.2f}", True, (0, 0, 0))
        window.blit(button_text, (button_x + 10, button_y + 10))
        
    pygame.display.flip()

pygame.quit()
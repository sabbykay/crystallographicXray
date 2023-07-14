import pygame 
pygame.init()

width = 800
height = 600 
window = pygame.display.set_mode((width, height))

running = True
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    window.fill((0, 0, 0))
    pygame.display.flip()

pygame.quit()
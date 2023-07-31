import pygame

pygame.init()

screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Hellow World")

done = False
while not done:
    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            done = True
    pygame.display.update()
    
pygame.quit()
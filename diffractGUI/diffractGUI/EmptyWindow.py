import pygame

def setup():
    pygame.init()
    display_width, display_height = 800, 600
    pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("Hellow Window")
    window = (255, 255, 255)

def main():
    setup()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                window.fill((255, 255, 255))
                pygame.display.update()

if __name__ == '__main__':
    main()
import pygame
from clifford import Cl

pygame.init()

width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Diffractometer Controls")  # Set the window title

# Set up the scene
scene = Cl(3)

# Define initial angles
angles = [0, 0, 0]

button_width = 200
button_height = 30
button_padding = 15

button_positions = [
    (button_padding, button_padding),
    (button_padding, 2 * button_padding + button_height),
    (button_padding, 3 * button_padding + 2 * button_height),
    (button_padding, 4 * button_padding + 3 * button_height),
    (button_padding, 5 * button_padding + 4 * button_height),
    (button_padding, 6 * button_padding + 5 * button_height),
]

button_color = (100, 100, 100)
button_hover_color = (150, 150, 150)


# Increment angle function
def increment_angle(index):
    angles[index] += 0.1


# Decrement angle function
def decrement_angle(index):
    angles[index] -= 0.1


# Check button click function
def check_button_click(mouse_pos, index):
    button_x, button_y = button_positions[index]
    return (
        button_x <= mouse_pos[0] <= button_x + button_width
        and button_y <= mouse_pos[1] <= button_y + button_height
    )


button_labels = ["Angle 1 +", "Angle 1 -", "Angle 2 +", "Angle 2 -", "Angle 3 +", "Angle 3 -"]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check for mouse button clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()

                # Check if any button is clicked
                for i in range(len(button_positions)):
                    if check_button_click(mouse_pos, i):
                        if i % 2 == 0:
                            increment_angle(i // 2)
                        else:
                            decrement_angle(i // 2)

    window.fill((255, 255, 255))

    # Render the buttons and labels
    for i, position in enumerate(button_positions):
        button_x, button_y = position
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        button_color_to_use = button_hover_color if check_button_click(pygame.mouse.get_pos(), i) else button_color
        pygame.draw.rect(window, button_color_to_use, button_rect)

        # Render button text
        font = pygame.font.Font(None, 20)
        button_text = font.render(f"{button_labels[i]}: {angles[i // 2]:.2f}", True, (0, 0, 0))
        text_width, text_height = font.size(button_labels[i])
        text_x = button_x + (button_width - text_width) // 2
        text_y = button_y + (button_height - text_height) // 2
        window.blit(button_text, (text_x, text_y))

    pygame.display.update()
pygame.quit()

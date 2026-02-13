import pygame
import subprocess
import sys

pygame.init()

# Screen setup
infoObject = pygame.display.Info()
screen_width = infoObject.current_w
screen_height = infoObject.current_h
screen = pygame.display.set_mode((screen_width - 100, screen_height - 100), pygame.RESIZABLE)
pygame.mouse.set_visible(True)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
LIGHT_GRAY = (200, 200, 200)

# Fonts
font_title = pygame.font.Font(None, 74)
font_button = pygame.font.Font(None, 60)

# Button layout
button_width = 400
button_height = 100
button_spacing = 30

def get_button_rects():
    screen_w, screen_h = screen.get_size()
    start_y = screen_h // 2 - (4 * button_height + 3 * button_spacing) // 2
    rects = []
    for i in range(4):
        rects.append(pygame.Rect(
            screen_w // 2 - button_width // 2,
            start_y + i * (button_height + button_spacing),
            button_width,
            button_height
        ))
    return rects

def draw_button(rect, text):
    mouse_pos = pygame.mouse.get_pos()
    color = LIGHT_GRAY if rect.collidepoint(mouse_pos) else GRAY
    pygame.draw.rect(screen, color, rect, border_radius=12)
    text_surface = font_button.render(text, True, BLACK)
    screen.blit(text_surface, text_surface.get_rect(center=rect.center))

def run_script(script_name):
    subprocess.Popen([sys.executable, script_name])
    pygame.quit()
    sys.exit()

experiment_names = [
    ("Experiment 1", "experiment1.py"),
    ("Experiment 2", "experiment2.py"),
    ("Experiment 3", "experiment3.py"),
    ("Experiment 4", "experiment4.py")
]

# Main loop
while True:
    button_rects = get_button_rects()
    screen.fill(BLACK)

    for i, (label, _) in enumerate(experiment_names):
        draw_button(button_rects[i], label)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, (_, script) in enumerate(experiment_names):
                if button_rects[i].collidepoint(event.pos):
                    run_script(script)

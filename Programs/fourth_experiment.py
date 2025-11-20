"""
The fourth experiment: Gray-scale gradients.
Dration: 5 seconds ((a), Preparation) + 3 seconds (changes to (d)) + 3 sconds (changes to (a))
The color combinations: 
    1.White and Black
    2.Red and Blue
    3.Yellow and Blue
    4.Red and Green 
    5.Green and Blue 
在一个实验中，两个颜色的对比度设定为100%
白色导致瞳孔扩张、黑色导致瞳孔收缩
Process:
    1.开始画面，附带说明文，点击空格开始
    2.从5s的(a)开始，经过3秒，渐变为(d)，再经过3秒，渐变回(a)
    3.重复步骤三10次（110s）
    4.摁下空格，开始下一组颜色组合
    5.重复3-4，直到5组颜色组合结束（共550s）
"""

import pygame
import time
import math

# Initialize Pygame
pygame.init()

# Screen setup (Full-screen windowed)
infoObject = pygame.display.Info()
screen_width = infoObject.current_w
screen_height = infoObject.current_h
screen = pygame.display.set_mode((screen_width-100, screen_height-100), pygame.RESIZABLE)
pygame.mouse.set_visible(True)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
LIGHT_GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Fonts
font_title = pygame.font.Font(None, 74)
font_counter = pygame.font.Font(None, 120)
font_text = pygame.font.Font(None, 50)

# Main menu button properties
button_width = 250
button_height = 80
button_y_offset = 50

# Global button rects, will be updated by reposition_elements
tutorial_button_rect = pygame.Rect(0, 0, 0, 0)
start_button_rect = pygame.Rect(0, 0, 0, 0)
exit_button_rect = pygame.Rect(0, 0, 0, 0)

# --- Define the color combinations ---
# The (WHITE, BLACK) combination is removed.
episode_list = [(RED, BLUE), (YELLOW, BLUE), (RED, GREEN), (GREEN, BLUE)]

def reposition_elements():
    """Recalculate and update the positions of all screen elements based on current window size."""
    global screen_width, screen_height, tutorial_button_rect, start_button_rect, exit_button_rect
    screen_width, screen_height = screen.get_size()
    
    # Recalculate main menu button rects
    tutorial_button_rect.topleft = (screen_width // 2 - button_width // 2, screen_height // 2 - button_height - button_y_offset)
    tutorial_button_rect.size = (button_width, button_height)
    
    start_button_rect.topleft = (screen_width // 2 - button_width // 2, screen_height // 2)
    start_button_rect.size = (button_width, button_height)
    
    exit_button_rect.topleft = (screen_width // 2 - button_width // 2, screen_height // 2 + button_height + button_y_offset)
    exit_button_rect.size = (button_width, button_height)

def draw_button(screen, rect, text, color, hover_color):
    mouse_pos = pygame.mouse.get_pos()
    button_color = hover_color if rect.collidepoint(mouse_pos) else color
    pygame.draw.rect(screen, button_color, rect, border_radius=10)
    text_surface = font_title.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def wait_for_space():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.VIDEORESIZE:
                reposition_elements()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                waiting = False

def show_text_screen(text, wait_for_input=True):
    screen.fill(BLACK)
    lines = text.split('\n')
    line_spacing = font_text.get_linesize()
    total_height = len(lines) * line_spacing
    start_y = (screen_height - total_height) // 2
    
    for i, line in enumerate(lines):
        text_surface = font_text.render(line, True, WHITE)
        text_rect = text_surface.get_rect(center=(screen_width // 2, start_y + i * line_spacing))
        screen.blit(text_surface, text_rect)
    
    if wait_for_input:
        space_text = font_text.render("Press Space Key", True, WHITE)
        space_rect = space_text.get_rect(center=(screen_width // 2, screen_height - 100))
        screen.blit(space_text, space_rect)
    
    pygame.display.flip()
    if wait_for_input:
        wait_for_space()

def get_interp_color(color1, color2, t):
    """Linear interpolation between two colors based on t (0.0 to 1.0)."""
    r = int(color1[0] * (1.0 - t) + color2[0] * t)
    g = int(color1[1] * (1.0 - t) + color2[1] * t)
    b = int(color1[2] * (1.0 - t) + color2[2] * t)
    return (r, g, b)

def generate_gradient_surface(base_color, contrast_color, progress):
    """Generates the gradient pattern based on a progress value (0.0 to 1.0)."""
    surface = pygame.Surface((screen_width, screen_height))
    square_size = min(screen_width, screen_height) // 4
    center_x, center_y = screen_width // 2, screen_height // 2
    
    # Draw the background
    bg_color = get_interp_color(base_color, contrast_color, progress)
    surface.fill(bg_color)
    
    # Define the 5 squares
    square_rects = [
        pygame.Rect(center_x - square_size // 2, center_y - square_size // 2, square_size, square_size),  # Center
        pygame.Rect(center_x - square_size // 2, center_y - square_size // 2 - square_size, square_size, square_size),  # Top
        pygame.Rect(center_x - square_size // 2, center_y - square_size // 2 + square_size, square_size, square_size),  # Bottom
        pygame.Rect(center_x - square_size // 2 - square_size, center_y - square_size // 2, square_size, square_size),  # Left
        pygame.Rect(center_x - square_size // 2 + square_size, center_y - square_size // 2, square_size, square_size)  # Right
    ]
    
    # Draw the central square (same color as the background/outside area)
    center_square_color = get_interp_color(base_color, contrast_color, progress)
    pygame.draw.rect(surface, center_square_color, square_rects[0])
    
    # Draw the four side squares with gradients (COMPLETELY REVERSED)
    # Top square: gradient from inner edge (background) to outer edge (contrast)
    for y in range(square_rects[1].height):
        t_pos = y / (square_rects[1].height - 1)
        inner_edge_color = get_interp_color(base_color, contrast_color, progress)  # Same as background
        outer_edge_color = get_interp_color(contrast_color, base_color, progress)  # Opposite of background
        # Start from inner (top edge), end at outer (bottom edge)
        color = get_interp_color(inner_edge_color, outer_edge_color, t_pos)
        pygame.draw.line(surface, color, (square_rects[1].x, square_rects[1].y + y), (square_rects[1].x + square_rects[1].width, square_rects[1].y + y))
    
    # Bottom square: gradient from outer edge (contrast) to inner edge (background)
    for y in range(square_rects[2].height):
        t_pos = y / (square_rects[2].height - 1)
        inner_edge_color = get_interp_color(base_color, contrast_color, progress)  # Same as background
        outer_edge_color = get_interp_color(contrast_color, base_color, progress)  # Opposite of background
        # Start from outer (top edge), end at inner (bottom edge)
        color = get_interp_color(outer_edge_color, inner_edge_color, t_pos)
        pygame.draw.line(surface, color, (square_rects[2].x, square_rects[2].y + y), (square_rects[2].x + square_rects[2].width, square_rects[2].y + y))
    
    # Left square: gradient from inner edge (background) to outer edge (contrast)
    for x in range(square_rects[3].width):
        t_pos = x / (square_rects[3].width - 1)
        inner_edge_color = get_interp_color(base_color, contrast_color, progress)  # Same as background
        outer_edge_color = get_interp_color(contrast_color, base_color, progress)  # Opposite of background
        # Start from inner (left edge), end at outer (right edge)
        color = get_interp_color(inner_edge_color, outer_edge_color, t_pos)
        pygame.draw.line(surface, color, (square_rects[3].x + x, square_rects[3].y), (square_rects[3].x + x, square_rects[3].y + square_rects[3].height))
    
    # Right square: gradient from outer edge (contrast) to inner edge (background)
    for x in range(square_rects[4].width):
        t_pos = x / (square_rects[4].width - 1)
        inner_edge_color = get_interp_color(base_color, contrast_color, progress)  # Same as background
        outer_edge_color = get_interp_color(contrast_color, base_color, progress)  # Opposite of background
        # Start from outer (left edge), end at inner (right edge)
        color = get_interp_color(outer_edge_color, inner_edge_color, t_pos)
        pygame.draw.line(surface, color, (square_rects[4].x + x, square_rects[4].y), (square_rects[4].x + x, square_rects[4].y + square_rects[4].height))
    
    # Draw the black fixation cross in the center
    cross_color = BLACK
    cross_length = square_size // 10
    cross_thickness = 17
    pygame.draw.line(surface, cross_color, (center_x - cross_length, center_y), (center_x + cross_length, center_y), cross_thickness)
    pygame.draw.line(surface, cross_color, (center_x, center_y - cross_length), (center_x, center_y + cross_length), cross_thickness)
    
    return surface

def run_gradient_experiment(episodes, show_finish_screen=True):
    finish_text = font_title.render("Finish. Press the Space key to exit", True, WHITE)
    
    for i, (base_color, contrast_color) in enumerate(episodes):
        for repeat_count in range(10):
            print(f"Starting Episode {i+1}, Repetition {repeat_count+1}/10")
            
            # Use screen.get_size() for dynamic dimensions
            dynamic_screen_width, dynamic_screen_height = screen.get_size()
            
            # Part 1: Initial State 1 display for 5 seconds
            start_time = time.time()
            while time.time() - start_time < 5:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.VIDEORESIZE:
                        reposition_elements()
                
                gradient_surface = generate_gradient_surface(base_color, contrast_color, progress=0.0)
                screen.blit(gradient_surface, (0, 0))
                pygame.display.flip()
            
            # Part 2: Transition from State 1 to State 2 over 3 seconds
            fade_duration = 3.0
            start_time = time.time()
            while time.time() - start_time < fade_duration:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.VIDEORESIZE:
                        reposition_elements()
                
                elapsed = time.time() - start_time
                progress = elapsed / fade_duration
                gradient_surface = generate_gradient_surface(base_color, contrast_color, progress)
                screen.blit(gradient_surface, (0, 0))
                pygame.display.flip()
            
            # Part 3: Transition from State 2 to State 1 over 3 seconds
            start_time = time.time()
            while time.time() - start_time < fade_duration:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.VIDEORESIZE:
                        reposition_elements()
                
                elapsed = time.time() - start_time
                progress = 1.0 - (elapsed / fade_duration)
                gradient_surface = generate_gradient_surface(base_color, contrast_color, progress)
                screen.blit(gradient_surface, (0, 0))
                pygame.display.flip()
        
        if i < len(episodes) - 1:
            next_episode_num = i + 2
            line1_text = f"Episode {i+1} finished."
            line2_text = f"Press Space Key to Start Episode {next_episode_num}"
            show_text_screen(line1_text + '\n' + line2_text)
    
    if show_finish_screen:
        screen.fill(BLACK)
        finish_text_rect = finish_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(finish_text, finish_text_rect)
        pygame.display.flip()
        wait_for_space()

# --- Main loop and state machine ---
reposition_elements()  # Initial call to position everything
state = "menu"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.VIDEORESIZE:
            reposition_elements()
        
        if state == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if tutorial_button_rect.collidepoint(event.pos):
                    state = "tutorial"
                elif start_button_rect.collidepoint(event.pos):
                    state = "start_experiment"
                elif exit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()
    
    if state == "menu":
        screen.fill(BLACK)
        draw_button(screen, tutorial_button_rect, "Tutorial", GRAY, LIGHT_GRAY)
        draw_button(screen, start_button_rect, "Start", GRAY, LIGHT_GRAY)
        draw_button(screen, exit_button_rect, "Exit", GRAY, LIGHT_GRAY)
        pygame.display.flip()
    
    elif state == "tutorial":
        show_text_screen("This program measures pupil changes.\n Please make sure you have no eye diseases.")
        show_text_screen("A gradient pattern will appear.\n It will fade in contrast and then fade back.\n Keep your eyes on the center cross.")
        
        # Modified tutorial loop: 1 repetition
        base_color, contrast_color = episode_list[0]
        for repeat_count in range(1):
            start_time = time.time()
            while time.time() - start_time < 5:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.VIDEORESIZE:
                        reposition_elements()
                
                gradient_surface = generate_gradient_surface(base_color, contrast_color, progress=0.0)
                screen.blit(gradient_surface, (0, 0))
                pygame.display.flip()
            
            fade_duration = 3.0
            start_time = time.time()
            while time.time() - start_time < fade_duration:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.VIDEORESIZE:
                        reposition_elements()
                
                elapsed = time.time() - start_time
                progress = elapsed / fade_duration
                gradient_surface = generate_gradient_surface(base_color, contrast_color, progress)
                screen.blit(gradient_surface, (0, 0))
                pygame.display.flip()
            
            start_time = time.time()
            while time.time() - start_time < fade_duration:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.VIDEORESIZE:
                        reposition_elements()
                
                elapsed = time.time() - start_time
                progress = 1.0 - (elapsed / fade_duration)
                gradient_surface = generate_gradient_surface(base_color, contrast_color, progress)
                screen.blit(gradient_surface, (0, 0))
                pygame.display.flip()
        
        show_text_screen("There are 5 color combinations in total. \n After one finish, press the space bar to proceed to the next combination. \n\n Time required for each combination: 50 seconds. \n Total time required: 4 minutes 20 seconds")
        show_text_screen("Tutorial complete. \n Press the spacebar to return to the main menu.")
        state = "menu"
    
    elif state == "start_experiment":
        run_gradient_experiment(episodes=episode_list)
        state = "menu"
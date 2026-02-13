import pygame
import time
import random
import math

# Initialize Pygame
pygame.init()

# Screen setup (Full-screen windowed)
infoObject = pygame.display.Info()
screen_width_full = infoObject.current_w
screen_height_full = infoObject.current_h
screen = pygame.display.set_mode((screen_width_full - 100, screen_height_full - 100), pygame.RESIZABLE)
pygame.mouse.set_visible(True)

# Path to the parent image directory
imgDir = 'Images\\Experiment3\\ColorCombination'

# List of episode numbers to run
episode_list = [1, 2, 3, 4]

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
LIGHT_GRAY = (200, 200, 200)

# Fonts
font_title = pygame.font.Font(None, 74)
font_counter = pygame.font.Font(None, 120)
font_text = pygame.font.Font(None, 50)

# Main menu button properties
button_width = 250
button_height = 80
button_y_offset = 50

# Buttons' rects, now calculated dynamically
def get_button_rects():
    screen_w, screen_h = screen.get_size()
    tutorial_button_rect = pygame.Rect(
        screen_w // 2 - button_width // 2,
        screen_h // 2 - button_height - button_y_offset,
        button_width,
        button_height
    )
    start_button_rect = pygame.Rect(
        screen_w // 2 - button_width // 2,
        screen_h // 2,
        button_width,
        button_height
    )
    exit_button_rect = pygame.Rect(
        screen_w // 2 - button_width // 2,
        screen_h // 2 + button_height + button_y_offset,
        button_width,
        button_height
    )
    return tutorial_button_rect, start_button_rect, exit_button_rect

# --- New parameters for the experiment ---
screen_width_cm = 61.2
screen_height_cm = 34.4
eye_distance_cm = 66
screen_width_pixel = 1920
screen_height_pixel = 1080

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                waiting = False
            
def show_text_screen(text, wait_for_input=True):
    screen.fill(BLACK)
    screen_w, screen_h = screen.get_size()
    lines = text.split('\n')
    line_spacing = font_text.get_linesize()
    total_height = len(lines) * line_spacing
    start_y = (screen_h - total_height) // 2
    
    for i, line in enumerate(lines):
        text_surface = font_text.render(line, True, WHITE)
        text_rect = text_surface.get_rect(center=(screen_w // 2, start_y + i * line_spacing))
        screen.blit(text_surface, text_rect)

    if wait_for_input:
        space_text = font_text.render("Press Space Key", True, WHITE)
        space_rect = space_text.get_rect(center=(screen_w // 2, screen_h - 100))
        screen.blit(space_text, space_rect)
        
    pygame.display.flip()
    if wait_for_input:
        wait_for_space()
    
def scale_to_fit(image_surface, target_size):
    image_rect = image_surface.get_rect()
    target_width, target_height = target_size
    
    scale_factor = min(target_width / image_rect.width, target_height / image_rect.height)
    
    new_width = int(image_rect.width * scale_factor)
    new_height = int(image_rect.height * scale_factor)
    
    scaled_image = pygame.transform.scale(image_surface, (new_width, new_height))
    
    return scaled_image

def show_image_with_counter(image, duration, counter_text, counter_number):
    screen_w, screen_h = screen.get_size()
    start_time = time.time()
    image_rect = image.get_rect(center=(screen_w // 2, screen_h // 2))
    
    counter_number_surface = font_counter.render(counter_number, True, (0, 0, 0))
    counter_text_surface = font_counter.render(counter_text, True, (0, 0, 0))
    counter_number_rect = counter_text_surface.get_rect(center=(screen_w // 1.7, screen_h // 2.4))
    counter_text_rect = counter_text_surface.get_rect(center=(screen_w // 2, screen_h // 2))
    
    while time.time() - start_time < 5:
        screen.fill(BLACK)
        screen.blit(image, image_rect)
        screen.blit(counter_number_surface, counter_number_rect)
        screen.blit(counter_text_surface, counter_text_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

# --- NEW FUNCTION FOR THE EXPERIMENT ---
def run_new_experiment(episodes, repetitions_per_episode=10, shapes_per_repetition=5, show_finish_screen=True):
    screen_w, screen_h = screen.get_size()
    finish_text = font_title.render("Finish. Press the Space key to exit", True, (255, 255, 255))
    finish_text_rect = finish_text.get_rect(center=(screen_w // 2, screen_h // 2))

    # Calculate pixel speed
    visual_angle_rad = math.radians(50)
    screen_width_rad = 2 * math.atan((screen_width_cm / 2) / eye_distance_cm)
    pixels_per_radian = screen_width_pixel / screen_width_rad
    speed_in_pixels_per_second = visual_angle_rad * pixels_per_radian
    
    shape_files = ["Circle.png", "Square.png", "Triangle.png", "Star.png"]

    for i in range(len(episodes)):
        episode = episodes[i]
        next_episode = episodes[i + 1] if i < len(episodes) - 1 else None

        print(f"Starting Episode {episode}")
        
        try:
            background_image_raw = pygame.image.load(imgDir + str(episode) + '\\BackgroundColor.png').convert()
            shapes = {
                "Circle": pygame.image.load(imgDir + str(episode) + '\\Circle.png').convert_alpha(),
                "Square": pygame.image.load(imgDir + str(episode) + '\\Square.png').convert_alpha(),
                "Triangle": pygame.image.load(imgDir + str(episode) + '\\Triangle.png').convert_alpha(),
                "Star": pygame.image.load(imgDir + str(episode) + '\\Star.png').convert_alpha()
            }
        except pygame.error as e:
            print(f"Error loading images for episode {episode}: {e}")
            continue

        background_image = pygame.transform.scale(background_image_raw, (screen_w, screen_h))
        
        # New loop for the repetitions
        for _ in range(repetitions_per_episode):
            # 2. 播放5s纯色
            show_image_with_counter(background_image, 5, "Get Ready", str(_ + 1))
            # 3. 播放图形移动5次
            for j in range(shapes_per_repetition):
                random_shape_name = random.choice(shape_files)
                moving_shape = shapes[random_shape_name.split('.')[0]]
                shape_rect = moving_shape.get_rect()
                shape_rect.x = -shape_rect.width
                shape_rect.centery = screen_h // 2

                clock = pygame.time.Clock()
                is_moving = True
                
                while is_moving:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        
                    screen.blit(background_image, (0, 0))
                    screen.blit(moving_shape, shape_rect)
                    pygame.display.flip()

                    shape_rect.x += speed_in_pixels_per_second * (clock.get_time() / 1000.0)
                    if shape_rect.x > screen_w:
                        is_moving = False

                    clock.tick(60)

        if next_episode:
            line1_text = f"The episode {episode} finished."
            line2_text = f"Press Space Key to Start the Episode {next_episode}"
            show_text_screen(line1_text + '\n' + line2_text)

    if show_finish_screen:
        screen.fill(BLACK)
        screen.blit(finish_text, finish_text_rect)
        pygame.display.flip()
        wait_for_space()

# --- Main loop and state machine ---
state = "menu"
while True:
    if state == "menu":
        tutorial_button_rect, start_button_rect, exit_button_rect = get_button_rects()
        screen.fill(BLACK)
        draw_button(screen, tutorial_button_rect, "Tutorial", GRAY, LIGHT_GRAY)
        draw_button(screen, start_button_rect, "Start", GRAY, LIGHT_GRAY)
        draw_button(screen, exit_button_rect, "Exit", GRAY, LIGHT_GRAY)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if tutorial_button_rect.collidepoint(event.pos):
                    state = "tutorial"
                elif start_button_rect.collidepoint(event.pos):
                    state = "start_experiment"
                elif exit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()
            if event.type == pygame.VIDEORESIZE:
                screen_w, screen_h = event.size
                screen = pygame.display.set_mode((screen_w, screen_h), pygame.RESIZABLE)

    elif state == "tutorial":
        show_text_screen("This program measures pupil changes.\n Please make sure you have no eye diseases.")
        show_text_screen("A colored background will appear for 5 seconds.\n Then, a random shape will move from left to right.\n Keep your eyes on the moving shape.")
        
        run_new_experiment(episodes=[1], repetitions_per_episode=1, shapes_per_repetition=1, show_finish_screen=False)
        
        show_text_screen("In the real experiment, \n for each color combination, the background will appear for 5 seconds, followed by 5 moving shapes, repeating this 10 times.")
        
        show_text_screen("There are 4 color combinations in total. \n After one finishes, press the space bar to proceed to the next combination. \n\n Time required for each combination: 2 minutes. \n Total time required: 8 minutes")

        show_text_screen("Tutorial complete. \n Press the spacebar to return to the main menu.")
        state = "menu"
        
    elif state == "start_experiment":
        run_new_experiment(episodes=episode_list)
        state = "menu"
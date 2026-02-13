import pygame
import time

# Initialize Pygame
pygame.init()

# Screen setup (Full-screen windowed)
infoObject = pygame.display.Info()
screen_width_full = infoObject.current_w
screen_height_full = infoObject.current_h
screen = pygame.display.set_mode((screen_width_full-100, screen_height_full-100), pygame.RESIZABLE)
pygame.mouse.set_visible(True)

# Path to the parent image directory
imgDir = 'Images\\Experiment1\\ColorCombination'

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

def show_image_with_counter(image, duration, counter_text):
    screen_w, screen_h = screen.get_size()
    start_time = time.time()
    image_rect = image.get_rect(center=(screen_w // 2, screen_h // 2))
    
    counter_surface = font_counter.render(counter_text, True, (0, 0, 0))
    counter_rect = counter_surface.get_rect(center=(screen_w // 2, screen_h // 2.3))

    while time.time() - start_time < 5:
        screen.fill(BLACK)
        screen.blit(image, image_rect)
        screen.blit(counter_surface, counter_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

def flicker_images(image1, image2, duration, frequency):
    screen_w, screen_h = screen.get_size()
    start_time = time.time()
    interval = 1.0 / (2 * frequency)
    current_image = image1
    last_switch_time = start_time

    image1_rect = image1.get_rect(center=(screen_w // 2, screen_h // 2))
    image2_rect = image2.get_rect(center=(screen_w // 2, screen_h // 2))

    while time.time() - start_time < 5:
        screen.fill(BLACK)
        if current_image == image1:
            screen.blit(image1, image1_rect)
        else:
            screen.blit(image2, image2_rect)
        pygame.display.flip()

        current_time = time.time()
        if current_time - last_switch_time > interval:
            current_image = image2 if current_image == image1 else image1
            last_switch_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

def run_experiment(episodes, repetitions=10, show_finish_screen=True):
    screen_w, screen_h = screen.get_size()
    finish_text = font_title.render("Finish. Press the Space key to exit", True, (255, 255, 255))
    finish_text_rect = finish_text.get_rect(center=(screen_w // 2, screen_h // 2))

    for i in range(len(episodes)):
        episode = episodes[i]
        next_episode = episodes[i + 1] if i < len(episodes) - 1 else None

        print(f"Starting Episode {episode}")

        try:
            backgroundColor_raw = pygame.image.load(imgDir + str(episode) + '\\BackgroundColor.png').convert()
            frontColor_raw = pygame.image.load(imgDir + str(episode) + '\\FrontColor.png').convert()
            medianColor_raw = pygame.image.load(imgDir + str(episode) + '\\MedianColor.png').convert()
        except pygame.error as e:
            print(f"Error loading images for episode {episode}: {e}")
            continue

        backgroundColor = scale_to_fit(backgroundColor_raw, (screen_w, screen_h))
        frontColor = scale_to_fit(frontColor_raw, (screen_w, screen_h))
        medianColor = scale_to_fit(medianColor_raw, (screen_w, screen_h))

        for j in range(1, repetitions + 1):
            show_image_with_counter(medianColor, 5, str(j))
            flicker_images(backgroundColor, frontColor, 5, 3)

        if next_episode:
            line1_text = f"The episode {episode} finished."
            line2_text = f"Press Space Key to Start the Episode {next_episode}"
            show_text_screen(line1_text + '\n' + line2_text)

    if show_finish_screen:
        screen.fill(BLACK)
        screen.blit(finish_text, finish_text_rect)
        pygame.display.flip()
        wait_for_space()

def run_tutorial():
    show_text_screen("This program is supposed to measure the changes of human's pupil diameter.\n Please make sure you have no eye diseases.")

    show_text_screen("The next screen will display a solid-color background for 5 seconds. \n After that, two colors will alternate flashing for about 5 seconds. \n All you need to do is keep your eyes fixed on the cursor in the center.")

    run_experiment(episodes=[1], repetitions=1, show_finish_screen=False)

    show_text_screen("The number of attempts is displayed above the cursor. \n Repeat 20 times for each color combination.")

    show_text_screen("There are 4 combinations in total. \n Press the space bar to proceed to the next combination. \n\n Time required for each combination: 3 minute 20 seconds. \n Total time required: 13 minutes 20 seconds")

    show_text_screen("Tutorial complete. \n Press the spacebar to return to the main menu.")

    return "menu"

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
        run_tutorial()
        state = "menu"

    elif state == "start_experiment":
        run_experiment(episodes=episode_list)
        state = "menu"
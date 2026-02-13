import pygame
import sys
import time
import random

# ===================== Global Config =====================
number_of_set = 5 
time_of_preparation = 2
time_of_stimulus = 2

# ===================== Init =====================
pygame.init()
infoObject = pygame.display.Info()
screen = pygame.display.set_mode(
    (infoObject.current_w - 100, infoObject.current_h - 100),
    pygame.RESIZABLE
)
pygame.mouse.set_visible(True)

screen_width, screen_height = screen.get_size()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
LIGHT_GRAY = (200, 200, 200)

# Fonts
font_text = pygame.font.Font(None, 50)

# Button properties
button_width = 250
button_height = 80
button_y_offset = 30
column_gap = 80

# Image Paths
IMG_BG = "Images\\Experiment2\\Stimulus1\\Background.png"
IMG_FRONT = "Images\\Experiment2\\Stimulus1\\Front.png"


def handle_resize(event):
    global screen, screen_width, screen_height
    screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
    screen_width, screen_height = screen.get_size()


def wait_any_key():
    """等待任意键或鼠标点击"""
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                handle_resize(event)
            if event.type == pygame.KEYDOWN or \
               (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                waiting = False


def show_center_message(text):
    screen.fill(BLACK)
    lines = text.split("\n")
    total_height = len(lines) * font_text.get_linesize()
    start_y = screen_height // 2 - total_height // 2

    for i, line in enumerate(lines):
        surface = font_text.render(line, True, WHITE)
        rect = surface.get_rect(center=(screen_width // 2,
                                        start_y + i * font_text.get_linesize()))
        screen.blit(surface, rect)

    pygame.display.flip()
    wait_any_key()


def draw_button(rect, text):
    mouse_pos = pygame.mouse.get_pos()
    color = LIGHT_GRAY if rect.collidepoint(mouse_pos) else GRAY
    pygame.draw.rect(screen, color, rect, border_radius=10)

    text_surface = pygame.font.Font(None, 55).render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def get_two_column_button_rects(labels):
    w, h = screen.get_size()
    rows = 4
    total_height = rows * button_height + (rows - 1) * button_y_offset
    start_y = h // 2 - total_height // 2

    left_x = w // 2 - button_width - column_gap // 2
    right_x = w // 2 + column_gap // 2

    rects = []
    for r in range(rows):
        rects.append(pygame.Rect(left_x,
                                 start_y + r * (button_height + button_y_offset),
                                 button_width, button_height))
    for r in range(rows):
        rects.append(pygame.Rect(right_x,
                                 start_y + r * (button_height + button_y_offset),
                                 button_width, button_height))
    return rects


# ===================== Stimulus 1 Logic =====================

def run_stimulus1():
    print("Stimulus 1 start")

    try:
        bg_raw = pygame.image.load(IMG_BG).convert()
        front_raw = pygame.image.load(IMG_FRONT).convert()
    except pygame.error as e:
        print(f"Image loading error: {e}")
        return

    # scale images dynamically after resizing as well
    def update_scaled_images():
        return (
            pygame.transform.scale(bg_raw, (screen_width, screen_height)),
            pygame.transform.scale(front_raw, (screen_width, screen_height))
        )

    bg, front = update_scaled_images()

    flicker_freq = 3
    flicker_interval = 1.0 / (2 * flicker_freq)

    for current_set in range(1, number_of_set + 1):

        print(f"Set {current_set} start")

        # 10 cycles in one set
        for cycle in range(10):

            # Phase 1: Background 2s
            start = time.time()
            while time.time() - start < time_of_preparation:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.VIDEORESIZE:
                        handle_resize(event)
                        bg, front = update_scaled_images()

                screen.blit(bg, (0, 0))
                pygame.display.flip()

            # Phase 2: Flicker 2s
            start = time.time()
            current = front
            last_switch = start

            while time.time() - start < time_of_stimulus:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.VIDEORESIZE:
                        handle_resize(event)
                        bg, front = update_scaled_images()

                if time.time() - last_switch > flicker_interval:
                    current = bg if current == front else front
                    last_switch = time.time()

                screen.blit(current, (0, 0))
                pygame.display.flip()

        print(f"Set {current_set} finished")
        if current_set < number_of_set:
            show_center_message(f"Set {current_set} finished.\nPress any key to continue")

    show_center_message(
        "Stimulus 1 finished.\nPress any key to return to the menu"
    )
    print("Stimulus 1 end")

# ===================== Stimulus 2 Logic =====================

IMG_BG2 = "Images\\Experiment2\\Stimulus2\\Background.png"
IMG_FRONT2 = "Images\\Experiment2\\Stimulus2\\Front.png"


def run_stimulus2():
    print("Stimulus 2 start")

    try:
        bg_raw = pygame.image.load(IMG_BG2).convert()
        front_raw = pygame.image.load(IMG_FRONT2).convert()
    except pygame.error as e:
        print(f"Image loading error: {e}")
        return

    # scale images on demand
    def update_scaled_images():
        return (
            pygame.transform.scale(bg_raw, (screen_width, screen_height)),
            pygame.transform.scale(front_raw, (screen_width, screen_height))
        )

    bg, front = update_scaled_images()

    flicker_freq = 3
    flicker_interval = 1.0 / (2 * flicker_freq)

    for current_set in range(1, number_of_set + 1):

        print(f"Set {current_set} start")

        # 10 cycles per set
        for cycle in range(10):

            # Phase 1: Background 2s
            start = time.time()
            while time.time() - start < time_of_preparation:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.VIDEORESIZE:
                        handle_resize(event)
                        bg, front = update_scaled_images()

                screen.blit(bg, (0, 0))
                pygame.display.flip()

            # Phase 2: Flicker 2s
            start = time.time()
            current = front
            last_switch = start

            while time.time() - start < time_of_stimulus:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.VIDEORESIZE:
                        handle_resize(event)
                        bg, front = update_scaled_images()

                if time.time() - last_switch > flicker_interval:
                    current = bg if current == front else front
                    last_switch = time.time()

                screen.blit(current, (0, 0))
                pygame.display.flip()

        print(f"Set {current_set} finished")
        if current_set < number_of_set:
            show_center_message(f"Set {current_set} finished.\nPress any key to continue")

    show_center_message(
        "Stimulus 2 finished.\nPress any key to return to the menu"
    )
    print("Stimulus 2 end")

# ===================== Stimulus 3 Logic =====================

import random
import math

IMG_BG3 = "Images\\Experiment2\\Stimulus3\\background.png"
IMG_SHAPES3 = [
    "Images\\Experiment2\\Stimulus3\\circle.png",
    "Images\\Experiment2\\Stimulus3\\Square.png",
    "Images\\Experiment2\\Stimulus3\\Star.png",
    "Images\\Experiment2\\Stimulus3\\Triangle.png"
]
 
# Physical properties
D_cm = 60.0        # viewing distance
screen_width_cm = 53.1  # approx 24" width in cm
screen_width_px = 1920  # horizontal resolution

speed_deg_per_s = 50.0  # 50°/s

# compute px/s
cm_per_deg = 2 * D_cm * math.tan(math.radians(1.0 / 2.0))
px_per_cm = screen_width_px / screen_width_cm
px_per_deg = cm_per_deg * px_per_cm
speed_px_per_s = speed_deg_per_s * px_per_deg


def run_stimulus3():
    print("Stimulus 3 start")

    try:
        bg_raw = pygame.image.load(IMG_BG3).convert()
        shape_raws = [pygame.image.load(path).convert_alpha()
                      for path in IMG_SHAPES3]
    except pygame.error as e:
        print(f"Image loading error: {e}")
        return

    def update_scaled_images():
        bg_scaled = pygame.transform.scale(bg_raw, (screen_width, screen_height))
        shapes_scaled = [pygame.transform.scale(img, img.get_rect().size)
                         for img in shape_raws]
        return bg_scaled, shapes_scaled

    bg, shapes = update_scaled_images()
    clock = pygame.time.Clock()

    for current_set in range(1, number_of_set + 1):
        for cycle in range(10):

            shape = random.choice(shapes)
            rect = shape.get_rect()

            rect.centery = screen_height * 0.5

            rect.x = -rect.width / 2 + 45 # 左贴边内部

            # ===== Countdown only (1s total) =====
            for countdown in list(range(time_of_preparation, 0, -1)):
                start = time.time()
                while time.time() - start < 1:
                    dt = clock.tick(60) / 1000.0
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.VIDEORESIZE:
                            handle_resize(event)
                            bg, shapes = update_scaled_images()
                            rect.x = int(-rect.width + 1)

                    screen.blit(bg, (0, 0))
                    screen.blit(shape, rect)

                    countdown_surf = font_text.render(
                        str(countdown), True, (0, 0, 0))
                    countdown_rect = countdown_surf.get_rect(center=rect.center)
                    screen.blit(countdown_surf, countdown_rect)

                    pygame.display.flip()

            # ===== Immediately move after countdown =====
            x_pos = float(rect.x)
            moving = True

            while moving:
                dt = clock.tick(60) / 1000.0
                dx = speed_px_per_s * dt
                x_pos += dx
                rect.x = int(x_pos)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.VIDEORESIZE:
                        handle_resize(event)
                        bg, shapes = update_scaled_images()

                screen.blit(bg, (0, 0))
                screen.blit(shape, rect)
                pygame.display.flip()

                if rect.left > screen_width:
                    moving = False

        if current_set < number_of_set:
            show_center_message(f"Set {current_set} finished.\nPress any key to continue")

    show_center_message("Stimulus 3 finished.\nPress any key to return to the menu")
    print("Stimulus 3 end")

# ===================== Stimulus 4 Logic =====================

BASE_COLOR_4 = (0, 70, 255)
CONTRAST_COLOR_4 = (225, 255, 0)

FADE_DURATION = 1.0  # 渐变 1 秒
STATIC_DURATION = 2.0
CYCLES_PER_SET = 10

def get_interp_color(c1, c2, t):
    t = max(0.0, min(1.0, float(t)))  # clamp

    r = int(c1[0] + (c2[0] - c1[0]) * t)
    g = int(c1[1] + (c2[1] - c1[1]) * t)
    b = int(c1[2] + (c2[2] - c1[2]) * t)

    # ensure valid 0-255
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))

    return (r, g, b)

def generate_gradient_surface_4(base_color, contrast_color, progress):
    w, h = screen.get_size()
    surface = pygame.Surface((w, h))

    square_size = min(w, h) // 4
    center_x, center_y = w // 2, h // 2

    bg_color = get_interp_color(base_color, contrast_color, progress)
    surface.fill(bg_color)

    square_rects = [
        pygame.Rect(center_x - square_size // 2,
                    center_y - square_size // 2,
                    square_size, square_size),
        pygame.Rect(center_x - square_size // 2,
                    center_y - square_size // 2 - square_size,
                    square_size, square_size),
        pygame.Rect(center_x - square_size // 2,
                    center_y - square_size // 2 + square_size,
                    square_size, square_size),
        pygame.Rect(center_x - square_size // 2 - square_size,
                    center_y - square_size // 2,
                    square_size, square_size),
        pygame.Rect(center_x - square_size // 2 + square_size,
                    center_y - square_size // 2,
                    square_size, square_size),
    ]

    center_square_color = bg_color
    pygame.draw.rect(surface, center_square_color, square_rects[0])

    inner_edge_color = bg_color
    outer_edge_color = get_interp_color(contrast_color, base_color, progress)

    for sq_idx, sq in enumerate(square_rects[1:], start=1):
        if sq_idx == 1 or sq_idx == 2:
            for y in range(sq.height):
                t_ratio = y / max(1, sq.height - 1)
                if sq_idx == 1:  # top
                    color = get_interp_color(inner_edge_color, outer_edge_color, t_ratio)
                else:  # bottom
                    color = get_interp_color(outer_edge_color, inner_edge_color, t_ratio)
                pygame.draw.line(surface, color,
                                 (sq.x, sq.y + y),
                                 (sq.x + sq.width, sq.y + y))
        else:
            for x in range(sq.width):
                t_ratio = x / max(1, sq.width - 1)
                if sq_idx == 3:  # left
                    color = get_interp_color(inner_edge_color, outer_edge_color, t_ratio)
                else:  # right
                    color = get_interp_color(outer_edge_color, inner_edge_color, t_ratio)
                pygame.draw.line(surface, color,
                                 (sq.x + x, sq.y),
                                 (sq.x + x, sq.y + sq.height))

    cross_color = BLACK
    cross_length = square_size // 10
    cross_thickness = 17
    pygame.draw.line(surface, cross_color,
                     (center_x - cross_length, center_y),
                     (center_x + cross_length, center_y),
                     cross_thickness)
    pygame.draw.line(surface, cross_color,
                     (center_x, center_y - cross_length),
                     (center_x, center_y + cross_length),
                     cross_thickness)

    return surface

def run_stimulus4():
    print("Stimulus 4 start")
    clock = pygame.time.Clock()

    for current_set in range(1, number_of_set + 1):

        for cycle in range(CYCLES_PER_SET):

            # 1) Static 2s
            start = time.time()
            while time.time() - start < time_of_preparation:
                dt = clock.tick(60)/1000.0
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                    if event.type == pygame.VIDEORESIZE:
                        handle_resize(event)

                surf = generate_gradient_surface_4(BASE_COLOR_4, CONTRAST_COLOR_4, 0.0)
                screen.blit(surf, (0, 0))
                pygame.display.flip()

            # 2) fade 1s (0 → 1)
            start = time.time()
            while time.time() - start < FADE_DURATION:
                dt = clock.tick(60)/1000.0
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                    if event.type == pygame.VIDEORESIZE:
                        handle_resize(event)

                progress = (time.time() - start) / FADE_DURATION
                surf = generate_gradient_surface_4(BASE_COLOR_4, CONTRAST_COLOR_4, progress)
                screen.blit(surf, (0, 0))
                pygame.display.flip()

            # 3) fade 1s (1 → 0)
            start = time.time()
            while time.time() - start < FADE_DURATION:
                dt = clock.tick(60)/1000.0
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                    if event.type == pygame.VIDEORESIZE:
                        handle_resize(event)

                progress = 1.0 - (time.time() - start) / FADE_DURATION
                surf = generate_gradient_surface_4(BASE_COLOR_4, CONTRAST_COLOR_4, progress)
                screen.blit(surf, (0, 0))
                pygame.display.flip()

        if current_set < number_of_set:
            show_center_message(f"Set {current_set} finished.\nPress any key to continue")

    show_center_message("Stimulus 4 finished.\nPress any key to return to the menu")
    print("Stimulus 4 end")

# ===================== Stimulus 5 Logic =====================

import pygame
import time
import sys

IMG_BG5 = "Images\\Experiment2\\Stimulus5\\Background.png"
IMG_FRONT5 = "Images\\Experiment2\\Stimulus5\\Front.png"

CYCLES_PER_SET_5 = 10
STATIC_TIME_5 = 2.0   # 2s background + 2s front


def run_stimulus5():
    print("Stimulus 5 start")

    try:
        bg_raw = pygame.image.load(IMG_BG5).convert()
        front_raw = pygame.image.load(IMG_FRONT5).convert()
    except pygame.error as e:
        print(f"Image loading error: {e}")
        return

    def scale_images():
        bg = pygame.transform.scale(bg_raw, (screen_width, screen_height))
        front = pygame.transform.scale(front_raw, (screen_width, screen_height))
        return bg, front

    bg, front = scale_images()
    clock = pygame.time.Clock()

    for current_set in range(1, number_of_set + 1):
        print(f"Set {current_set} start")

        for i in range(CYCLES_PER_SET_5):

            # Show background 2s
            start = time.time()
            while time.time() - start < time_of_preparation:
                clock.tick(60)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                    if event.type == pygame.VIDEORESIZE:
                        handle_resize(event)
                        bg, front = scale_images()

                screen.blit(bg, (0, 0))
                pygame.display.flip()

            # Show front 2s
            start = time.time()
            while time.time() - start < time_of_stimulus:
                clock.tick(60)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                    if event.type == pygame.VIDEORESIZE:
                        handle_resize(event)
                        bg, front = scale_images()

                screen.blit(front, (0, 0))
                pygame.display.flip()

        if current_set < number_of_set:
            show_center_message(
                f"Set {current_set} finished.\nPress any key to continue"
            )

    show_center_message("Stimulus 5 finished.\nPress any key to return to the menu")
    print("Stimulus 5 end")

# ===================== Stimulus 6 Logic =====================

IMG_BG6 = "Images\\Experiment2\\Stimulus6\\Background.png"
IMG_FRONT6 = "Images\\Experiment2\\Stimulus6\\Front.png"

CYCLES_PER_SET_6 = 10
STATIC_TIME_6 = 2.0


def run_stimulus6():
    print("Stimulus 6 start")

    try:
        bg_raw = pygame.image.load(IMG_BG6).convert()
        front_raw = pygame.image.load(IMG_FRONT6).convert()
    except pygame.error as e:
        print(f"Image loading error: {e}")
        return

    def scale_images():
        bg = pygame.transform.scale(bg_raw, (screen_width, screen_height))
        front = pygame.transform.scale(front_raw, (screen_width, screen_height))
        return bg, front

    bg, front = scale_images()
    clock = pygame.time.Clock()

    for current_set in range(1, number_of_set + 1):
        print(f"Set {current_set} start")

        for cycle in range(CYCLES_PER_SET_6):
            
            # Background 2s
            start = time.time()
            while time.time() - start < time_of_preparation:
                clock.tick(60)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                    if event.type == pygame.VIDEORESIZE:
                        handle_resize(event)
                        bg, front = scale_images()
                screen.blit(bg, (0, 0))
                pygame.display.flip()

            # Front 2s
            start = time.time()
            while time.time() - start < time_of_stimulus:
                clock.tick(60)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                    if event.type == pygame.VIDEORESIZE:
                        handle_resize(event)
                        bg, front = scale_images()
                screen.blit(front, (0, 0))
                pygame.display.flip()

        if current_set < number_of_set:
            show_center_message(
                f"Set {current_set} finished.\nPress any key to continue"
            )

    show_center_message("Stimulus 6 finished.\nPress any key to return to the menu")
    print("Stimulus 6 end")

# ===================== Stimulus 7 Logic =====================

IMG_BG7 = "Images\\Experiment2\\Stimulus7\\Background.png"
IMG_FRONT7 = "Images\\Experiment2\\Stimulus7\\Front.png"

CYCLES_PER_SET_7 = 10
STATIC_TIME_7 = 2.0


def run_stimulus7():
    print("Stimulus 7 start")

    try:
        bg_raw = pygame.image.load(IMG_BG7).convert()
        front_raw = pygame.image.load(IMG_FRONT7).convert()
    except pygame.error as e:
        print(f"Image loading error: {e}")
        return

    def scale_images():
        bg = pygame.transform.scale(bg_raw, (screen_width, screen_height))
        front = pygame.transform.scale(front_raw, (screen_width, screen_height))
        return bg, front

    bg, front = scale_images()
    clock = pygame.time.Clock()

    for current_set in range(1, number_of_set + 1):
        print(f"Set {current_set} start")

        for cycle in range(CYCLES_PER_SET_7):

            # Background
            start = time.time()
            while time.time() - start < time_of_preparation:
                clock.tick(60)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                    if event.type == pygame.VIDEORESIZE:
                        handle_resize(event)
                        bg, front = scale_images()
                screen.blit(bg, (0, 0))
                pygame.display.flip()

            # Front
            start = time.time()
            while time.time() - start < time_of_stimulus:
                clock.tick(60)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                    if event.type == pygame.VIDEORESIZE:
                        handle_resize(event)
                        bg, front = scale_images()
                screen.blit(front, (0, 0))
                pygame.display.flip()

        if current_set < number_of_set:
            show_center_message(
                f"Set {current_set} finished.\nPress any key to continue"
            )

    show_center_message("Stimulus 7 finished.\nPress any key to return to the menu")
    print("Stimulus 7 end")

# ===================== Stimulus 8 Logic =====================

IMG_BG8 = "Images\\Experiment2\\Stimulus8\\Background.png"
IMG_FRONT8_1 = "Images\\Experiment2\\Stimulus8\\Front1.png"
IMG_FRONT8_2 = "Images\\Experiment2\\Stimulus8\\Front2.png"
IMG_FRONT8_3 = "Images\\Experiment2\\Stimulus8\\Front3.png"
IMG_FRONT8_4 = "Images\\Experiment2\\Stimulus8\\Front4.png"

CYCLES_PER_SET_8 = 10
STATIC_TIME_8 = 2.0

front_raw = []

def run_stimulus8():
    print("Stimulus 8 start")

    try:
        bg_raw = pygame.image.load(IMG_BG8).convert()
        for _ in range(4):
            front_raw.append(pygame.image.load(IMG_FRONT8_1).convert())
            front_raw.append(pygame.image.load(IMG_FRONT8_2).convert())
            front_raw.append(pygame.image.load(IMG_FRONT8_3).convert())
            front_raw.append(pygame.image.load(IMG_FRONT8_4).convert())
    except pygame.error as e:
        print(f"Image loading error: {e}")
        return

    def scale_images():
        bg = pygame.transform.scale(bg_raw, (screen_width, screen_height))
        front = pygame.transform.scale(front_raw[random.randint(1, 4)], (screen_width, screen_height))
        return bg, front

    clock = pygame.time.Clock()

    for current_set in range(1, number_of_set + 1):
        print(f"Set {current_set} start")

        for cycle in range(CYCLES_PER_SET_8):
            bg, front = scale_images()
            # Show BG 2s
            start = time.time()
            while time.time() - start < time_of_preparation:
                clock.tick(60)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                    if event.type == pygame.VIDEORESIZE:
                        handle_resize(event)
                        bg, front = scale_images()
                screen.blit(bg, (0, 0))
                pygame.display.flip()

            # Show Front 2s
            start = time.time()
            while time.time() - start < time_of_stimulus:
                clock.tick(60)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                    if event.type == pygame.VIDEORESIZE:
                        handle_resize(event)
                        bg, front = scale_images()
                screen.blit(front, (0, 0))
                pygame.display.flip()

        if current_set < number_of_set:
            show_center_message(
                f"Set {current_set} finished.\nPress any key to continue"
            )

    show_center_message("Stimulus 8 finished.\nPress any key to return to the menu")
    print("Stimulus 8 end")

# ===================== Main State Machine =====================

def main():
    state = "main_menu"

    while True:
        if state == "main_menu":
            labels = [
                "Stimulus 1", "Stimulus 2", "Stimulus 3", "Stimulus 4",
                "Stimulus 5", "Stimulus 6", "Stimulus 7", "Stimulus 8"
            ]
            rects = get_two_column_button_rects(labels)

            screen.fill(BLACK)
            for rect, label in zip(rects, labels):
                draw_button(rect, label)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    handle_resize(event)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if rects[0].collidepoint(event.pos):
                        run_stimulus1()
                        state = "main_menu"
                    elif rects[1].collidepoint(event.pos):
                        run_stimulus2()
                        state = "main_menu"
                    elif rects[2].collidepoint(event.pos):
                        run_stimulus3()
                        state = "main_menu"
                    elif rects[3].collidepoint(event.pos):  # Stimulus 4
                        run_stimulus4()
                        state = "main_menu"
                    elif rects[4].collidepoint(event.pos):
                        run_stimulus5()
                        state = "main_menu"
                    elif rects[5].collidepoint(event.pos):
                        run_stimulus6()
                        state = "main_menu"
                    elif rects[6].collidepoint(event.pos):
                        run_stimulus7()
                        state = "main_menu"
                    elif rects[7].collidepoint(event.pos):
                        run_stimulus8()
                        state = "main_menu"
                    else:
                        print("Other Stimulus button clicked (not implemented yet)")


if __name__ == "__main__":
    main()

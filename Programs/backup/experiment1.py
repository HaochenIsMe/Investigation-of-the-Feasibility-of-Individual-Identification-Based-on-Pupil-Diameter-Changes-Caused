import pygame
import time
import random
import math
import sys

# ===================== 初始化 & 全局资源 =====================

pygame.init()

infoObject = pygame.display.Info()
screen = pygame.display.set_mode((infoObject.current_w - 100,
                                  infoObject.current_h - 100),
                                 pygame.RESIZABLE)
pygame.mouse.set_visible(True)

screen_width, screen_height = screen.get_size()

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

# Button properties
button_width = 250
button_height = 80
button_y_offset = 50


def handle_resize(event):
    """统一处理窗口大小变更。"""
    global screen, screen_width, screen_height
    screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
    screen_width, screen_height = screen.get_size()


# ===================== 通用 UI 函数 =====================

def wait_for_space():
    """等待空格或鼠标左键，支持窗口 resize。"""
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                handle_resize(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                waiting = False


def show_text_screen(text, wait_for_input=True):
    """居中显示多行文本，底部提示 Press Space Key。"""
    screen.fill(BLACK)
    lines = text.split('\n')
    line_spacing = font_text.get_linesize()
    total_height = len(lines) * line_spacing
    start_y = (screen_height - total_height) // 2

    for i, line in enumerate(lines):
        text_surface = font_text.render(line, True, WHITE)
        text_rect = text_surface.get_rect(
            center=(screen_width // 2, start_y + i * line_spacing)
        )
        screen.blit(text_surface, text_rect)

    if wait_for_input:
        space_text = font_text.render("Press Space Key", True, WHITE)
        space_rect = space_text.get_rect(
            center=(screen_width // 2, screen_height - 100)
        )
        screen.blit(space_text, space_rect)

    pygame.display.flip()
    if wait_for_input:
        wait_for_space()


def draw_button(rect, text, base_color=GRAY, hover_color=LIGHT_GRAY):
    mouse_pos = pygame.mouse.get_pos()
    button_color = hover_color if rect.collidepoint(mouse_pos) else base_color
    pygame.draw.rect(screen, button_color, rect, border_radius=10)
    
    text_surface = pygame.font.Font(None, 55).render(text, True, BLACK)  # 用较小字体
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)



def get_three_button_rects():
    """返回当前窗口中垂直排列的3个按钮 rect（用于实验内部菜单）。"""
    w, h = screen.get_size()
    top = h // 2 - button_height - button_y_offset
    tutorial_button_rect = pygame.Rect(
        w // 2 - button_width // 2,
        top,
        button_width,
        button_height,
    )
    start_button_rect = pygame.Rect(
        w // 2 - button_width // 2,
        h // 2,
        button_width,
        button_height,
    )
    back_button_rect = pygame.Rect(
        w // 2 - button_width // 2,
        h // 2 + button_height + button_y_offset,
        button_width,
        button_height,
    )
    return tutorial_button_rect, start_button_rect, back_button_rect


def get_main_menu_button_rects(labels):
    """根据标签数量生成主菜单按钮 rect。"""
    w, h = screen.get_size()
    n = len(labels)
    total_height = n * button_height + (n - 1) * button_y_offset
    start_y = h // 2 - total_height // 2

    rects = []
    for i in range(n):
        rects.append(
            pygame.Rect(
                w // 2 - button_width // 2,
                start_y + i * (button_height + button_y_offset),
                button_width,
                button_height,
            )
        )
    return rects


def scale_to_fit(image_surface, target_size):
    image_rect = image_surface.get_rect()
    target_width, target_height = target_size
    scale_factor = min(target_width / image_rect.width,
                       target_height / image_rect.height)
    new_width = int(image_rect.width * scale_factor)
    new_height = int(image_rect.height * scale_factor)
    scaled_image = pygame.transform.scale(image_surface,
                                          (new_width, new_height))
    return scaled_image


# ===================== Experiment 1 =====================

IMG_DIR_EXP1 = 'Images\\Experiment1\\ColorCombination'
EPISODES_EXP1 = [1, 2, 3, 4]


def exp1_show_image_with_counter(image, duration, counter_text):
    screen_w, screen_h = screen.get_size()
    start_time = time.time()
    image_rect = image.get_rect(center=(screen_w // 2, screen_h // 2))

    counter_surface = font_counter.render(counter_text, True, BLACK)
    counter_rect = counter_surface.get_rect(
        center=(screen_w // 2, screen_h // 2.3)
    )

    # 原代码中 duration 未使用，这里保持 5 秒不动
    while time.time() - start_time < 5:
        screen.fill(BLACK)
        screen.blit(image, image_rect)
        screen.blit(counter_surface, counter_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                handle_resize(event)


def exp1_flicker_images(image1, image2, duration, frequency):
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
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                handle_resize(event)


def exp1_run_experiment(episodes, repetitions=10, show_finish_screen=True):
    screen_w, screen_h = screen.get_size()
    finish_text = font_title.render(
        "Finish. Press the Space key to exit", True, WHITE
    )
    finish_text_rect = finish_text.get_rect(
        center=(screen_w // 2, screen_h // 2)
    )

    for i in range(len(episodes)):
        episode = episodes[i]
        next_episode = episodes[i + 1] if i < len(episodes) - 1 else None

        print(f"[Experiment 1] Starting Episode {episode}")

        try:
            backgroundColor_raw = pygame.image.load(
                IMG_DIR_EXP1 + str(episode) + '\\BackgroundColor.png'
            ).convert()
            frontColor_raw = pygame.image.load(
                IMG_DIR_EXP1 + str(episode) + '\\FrontColor.png'
            ).convert()
            medianColor_raw = pygame.image.load(
                IMG_DIR_EXP1 + str(episode) + '\\MedianColor.png'
            ).convert()
        except pygame.error as e:
            print(f"Error loading images for episode {episode}: {e}")
            continue

        backgroundColor = scale_to_fit(backgroundColor_raw,
                                       (screen_w, screen_h))
        frontColor = scale_to_fit(frontColor_raw, (screen_w, screen_h))
        medianColor = scale_to_fit(medianColor_raw, (screen_w, screen_h))

        for j in range(1, repetitions + 1):
            exp1_show_image_with_counter(medianColor, 5, str(j))
            exp1_flicker_images(backgroundColor, frontColor, 5, 3)

        if next_episode:
            line1_text = f"The episode {episode} finished."
            line2_text = f"Press Space Key to Start the Episode {next_episode}"
            show_text_screen(line1_text + '\n' + line2_text)

    if show_finish_screen:
        screen.fill(BLACK)
        screen.blit(finish_text, finish_text_rect)
        pygame.display.flip()
        wait_for_space()


def exp1_run_tutorial():
    show_text_screen(
        "This program is supposed to measure the changes of human's pupil diameter.\n"
        " Please make sure you have no eye diseases."
    )

    show_text_screen(
        "The next screen will display a solid-color background for 5 seconds. \n"
        " After that, two colors will alternate flashing for about 5 seconds. \n"
        " All you need to do is keep your eyes fixed on the cursor in the center."
    )

    exp1_run_experiment(episodes=[1], repetitions=1, show_finish_screen=False)

    show_text_screen(
        "The number of attempts is displayed above the cursor. \n"
        " Repeat 20 times for each color combination."
    )

    show_text_screen(
        "There are 4 combinations in total. \n"
        " Press the space bar to proceed to the next combination. \n\n"
        " Time required for each combination: 3 minute 20 seconds. \n"
        " Total time required: 13 minutes 20 seconds"
    )

    show_text_screen(
        "Tutorial complete. \n"
        " Press the spacebar to return to the main menu."
    )


# ===================== Experiment 2 =====================

IMG_DIR_EXP2 = 'Images\\Experiment2\\ColorCombination'
EPISODES_EXP2 = [1, 2, 3, 4]


def exp2_show_image_with_counter(image, duration, counter_text):
    screen_w, screen_h = screen.get_size()
    start_time = time.time()
    image_rect = image.get_rect(center=(screen_w // 2, screen_h // 2))

    counter_surface = font_counter.render(counter_text, True, BLACK)
    counter_rect = counter_surface.get_rect(
        center=(screen_w // 2, screen_h // 2.3)
    )

    while time.time() - start_time < 5:
        screen.fill(BLACK)
        screen.blit(image, image_rect)
        screen.blit(counter_surface, counter_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                handle_resize(event)


def exp2_flicker_images(image1, image2, duration, frequency):
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
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                handle_resize(event)


def exp2_run_experiment(episodes, repetitions=10, show_finish_screen=True):
    screen_w, screen_h = screen.get_size()
    finish_text = font_title.render(
        "Finish. Press the Space key to exit", True, WHITE
    )
    finish_text_rect = finish_text.get_rect(
        center=(screen_w // 2, screen_h // 2)
    )

    for i in range(len(episodes)):
        episode = episodes[i]
        next_episode = episodes[i + 1] if i < len(episodes) - 1 else None

        print(f"[Experiment 2] Starting Episode {episode}")

        try:
            backgroundColor_raw = pygame.image.load(
                IMG_DIR_EXP2 + str(episode) + '\\BackgroundColor.png'
            ).convert()
            frontColor_raw = pygame.image.load(
                IMG_DIR_EXP2 + str(episode) + '\\FrontColor.png'
            ).convert()
        except pygame.error as e:
            print(f"Error loading images for episode {episode}: {e}")
            continue

        backgroundColor = scale_to_fit(backgroundColor_raw,
                                       (screen_w, screen_h))
        frontColor = scale_to_fit(frontColor_raw, (screen_w, screen_h))

        for j in range(1, repetitions + 1):
            exp2_show_image_with_counter(backgroundColor, 5, str(j))
            exp2_flicker_images(frontColor, backgroundColor, 5, 3)

        if next_episode:
            line1_text = f"The episode {episode} finished."
            line2_text = f"Press Space Key to Start the Episode {next_episode}"
            show_text_screen(line1_text + '\n' + line2_text)

    if show_finish_screen:
        screen.fill(BLACK)
        screen.blit(finish_text, finish_text_rect)
        pygame.display.flip()
        wait_for_space()


def exp2_run_tutorial():
    show_text_screen(
        "This program is supposed to measure the changes of human's pupil diameter.\n"
        " Please make sure you have no eye diseases."
    )

    show_text_screen(
        "The next screen will display a solid-color background for 5 seconds. \n"
        " After that, one colored ring will alternate flashing for about 5 seconds. \n"
        " All you need to do is keep your eyes fixed on the cursor in the center."
    )

    exp2_run_experiment(episodes=[1], repetitions=1, show_finish_screen=False)

    show_text_screen(
        "The number of attempts is displayed above the cursor. \n"
        " Repeat 20 times for each color combination."
    )

    show_text_screen(
        "There are 4 combinations in total. \n"
        " After one finish, Press the space bar to proceed to the next combination. \n\n"
        " Time required for each combination: 3 minute 20 seconds. \n"
        " Total time required: 13 minutes 20 seconds"
    )

    show_text_screen(
        "Tutorial complete. \n"
        " Press the spacebar to return to the main menu."
    )


# ===================== Experiment 3 =====================

IMG_DIR_EXP3 = 'Images\\Experiment3\\ColorCombination'
EPISODES_EXP3 = [1, 2, 3, 4]

# 实验参数（和你原来一致）
screen_width_cm = 61.2
screen_height_cm = 34.4
eye_distance_cm = 66
screen_width_pixel = 1920
screen_height_pixel = 1080


def exp3_show_image_with_counter(image, duration, counter_text, counter_number):
    screen_w, screen_h = screen.get_size()
    start_time = time.time()
    image_rect = image.get_rect(center=(screen_w // 2, screen_h // 2))

    counter_number_surface = font_counter.render(counter_number, True, BLACK)
    counter_text_surface = font_counter.render(counter_text, True, BLACK)
    counter_number_rect = counter_text_surface.get_rect(
        center=(screen_w // 1.7, screen_h // 2.4)
    )
    counter_text_rect = counter_text_surface.get_rect(
        center=(screen_w // 2, screen_h // 2)
    )

    while time.time() - start_time < 5:
        screen.fill(BLACK)
        screen.blit(image, image_rect)
        screen.blit(counter_number_surface, counter_number_rect)
        screen.blit(counter_text_surface, counter_text_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                handle_resize(event)


def exp3_run_new_experiment(episodes, repetitions_per_episode=10,
                            shapes_per_repetition=5,
                            show_finish_screen=True):
    screen_w, screen_h = screen.get_size()
    finish_text = font_title.render(
        "Finish. Press the Space key to exit", True, WHITE
    )
    finish_text_rect = finish_text.get_rect(
        center=(screen_w // 2, screen_h // 2)
    )

    # Calculate pixel speed
    visual_angle_rad = math.radians(50)
    screen_width_rad = 2 * math.atan((screen_width_cm / 2) / eye_distance_cm)
    pixels_per_radian = screen_width_pixel / screen_width_rad
    speed_in_pixels_per_second = visual_angle_rad * pixels_per_radian

    shape_files = ["Circle.png", "Square.png", "Triangle.png", "Star.png"]

    for i in range(len(episodes)):
        episode = episodes[i]
        next_episode = episodes[i + 1] if i < len(episodes) - 1 else None

        print(f"[Experiment 3] Starting Episode {episode}")

        try:
            background_image_raw = pygame.image.load(
                IMG_DIR_EXP3 + str(episode) + '\\BackgroundColor.png'
            ).convert()
            shapes = {
                "Circle": pygame.image.load(
                    IMG_DIR_EXP3 + str(episode) + '\\Circle.png'
                ).convert_alpha(),
                "Square": pygame.image.load(
                    IMG_DIR_EXP3 + str(episode) + '\\Square.png'
                ).convert_alpha(),
                "Triangle": pygame.image.load(
                    IMG_DIR_EXP3 + str(episode) + '\\Triangle.png'
                ).convert_alpha(),
                "Star": pygame.image.load(
                    IMG_DIR_EXP3 + str(episode) + '\\Star.png'
                ).convert_alpha(),
            }
        except pygame.error as e:
            print(f"Error loading images for episode {episode}: {e}")
            continue

        background_image = pygame.transform.scale(background_image_raw,
                                                  (screen_w, screen_h))

        for repetition in range(repetitions_per_episode):
            exp3_show_image_with_counter(
                background_image, 5, "Get Ready", str(repetition + 1)
            )
            for _ in range(shapes_per_repetition):
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
                            sys.exit()
                        if event.type == pygame.VIDEORESIZE:
                            handle_resize(event)

                    screen.blit(background_image, (0, 0))
                    screen.blit(moving_shape, shape_rect)
                    pygame.display.flip()

                    shape_rect.x += speed_in_pixels_per_second * (
                        clock.get_time() / 1000.0
                    )
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


def exp3_run_tutorial():
    show_text_screen(
        "This program measures pupil changes.\n"
        " Please make sure you have no eye diseases."
    )
    show_text_screen(
        "A colored background will appear for 5 seconds.\n"
        " Then, a random shape will move from left to right.\n"
        " Keep your eyes on the moving shape."
    )

    exp3_run_new_experiment(
        episodes=[1],
        repetitions_per_episode=1,
        shapes_per_repetition=1,
        show_finish_screen=False,
    )

    show_text_screen(
        "In the real experiment, \n"
        " for each color combination, the background will appear for 5 seconds, "
        "followed by 5 moving shapes, repeating this 10 times."
    )

    show_text_screen(
        "There are 4 color combinations in total. \n"
        " After one finishes, press the space bar to proceed to the next combination. \n\n"
        " Time required for each combination: 2 minutes. \n"
        " Total time required: 8 minutes"
    )

    show_text_screen(
        "Tutorial complete. \n"
        " Press the spacebar to return to the main menu."
    )


# ===================== Experiment 4 =====================

# (WHITE, BLACK) 被移除，按你给的代码
EPISODES_EXP4 = [(RED, BLUE), (YELLOW, BLUE), (RED, GREEN), (GREEN, BLUE)]


def get_interp_color(color1, color2, t):
    r = int(color1[0] * (1.0 - t) + color2[0] * t)
    g = int(color1[1] * (1.0 - t) + color2[1] * t)
    b = int(color1[2] * (1.0 - t) + color2[2] * t)
    return (r, g, b)


def generate_gradient_surface(base_color, contrast_color, progress):
    """与原 Experiment4 一致的渐变构造。"""
    surface = pygame.Surface((screen_width, screen_height))
    square_size = min(screen_width, screen_height) // 4
    center_x, center_y = screen_width // 2, screen_height // 2

    # 背景
    bg_color = get_interp_color(base_color, contrast_color, progress)
    surface.fill(bg_color)

    # 5 个方块区域
    square_rects = [
        pygame.Rect(center_x - square_size // 2,
                    center_y - square_size // 2,
                    square_size, square_size),  # Center
        pygame.Rect(center_x - square_size // 2,
                    center_y - square_size // 2 - square_size,
                    square_size, square_size),  # Top
        pygame.Rect(center_x - square_size // 2,
                    center_y - square_size // 2 + square_size,
                    square_size, square_size),  # Bottom
        pygame.Rect(center_x - square_size // 2 - square_size,
                    center_y - square_size // 2,
                    square_size, square_size),  # Left
        pygame.Rect(center_x - square_size // 2 + square_size,
                    center_y - square_size // 2,
                    square_size, square_size),  # Right
    ]

    # 中心方块 = 背景色
    center_square_color = get_interp_color(base_color,
                                           contrast_color,
                                           progress)
    pygame.draw.rect(surface, center_square_color, square_rects[0])

    # 与你给的代码相同的“完全反向渐变”
    # Top
    for y in range(square_rects[1].height):
        t_pos = y / (square_rects[1].height - 1)
        inner_edge_color = get_interp_color(base_color,
                                            contrast_color,
                                            progress)
        outer_edge_color = get_interp_color(contrast_color,
                                            base_color,
                                            progress)
        color = get_interp_color(inner_edge_color, outer_edge_color, t_pos)
        pygame.draw.line(
            surface, color,
            (square_rects[1].x, square_rects[1].y + y),
            (square_rects[1].x + square_rects[1].width,
             square_rects[1].y + y)
        )

    # Bottom
    for y in range(square_rects[2].height):
        t_pos = y / (square_rects[2].height - 1)
        inner_edge_color = get_interp_color(base_color,
                                            contrast_color,
                                            progress)
        outer_edge_color = get_interp_color(contrast_color,
                                            base_color,
                                            progress)
        color = get_interp_color(outer_edge_color, inner_edge_color, t_pos)
        pygame.draw.line(
            surface, color,
            (square_rects[2].x, square_rects[2].y + y),
            (square_rects[2].x + square_rects[2].width,
             square_rects[2].y + y)
        )

    # Left
    for x in range(square_rects[3].width):
        t_pos = x / (square_rects[3].width - 1)
        inner_edge_color = get_interp_color(base_color,
                                            contrast_color,
                                            progress)
        outer_edge_color = get_interp_color(contrast_color,
                                            base_color,
                                            progress)
        color = get_interp_color(inner_edge_color, outer_edge_color, t_pos)
        pygame.draw.line(
            surface, color,
            (square_rects[3].x + x, square_rects[3].y),
            (square_rects[3].x + x,
             square_rects[3].y + square_rects[3].height)
        )

    # Right
    for x in range(square_rects[4].width):
        t_pos = x / (square_rects[4].width - 1)
        inner_edge_color = get_interp_color(base_color,
                                            contrast_color,
                                            progress)
        outer_edge_color = get_interp_color(contrast_color,
                                            base_color,
                                            progress)
        color = get_interp_color(outer_edge_color, inner_edge_color, t_pos)
        pygame.draw.line(
            surface, color,
            (square_rects[4].x + x, square_rects[4].y),
            (square_rects[4].x + x,
             square_rects[4].y + square_rects[4].height)
        )

    # 中心 fixation cross
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


def exp4_run_gradient_experiment(episodes, show_finish_screen=True):
    finish_text = font_title.render(
        "Finish. Press the Space key to exit", True, WHITE
    )

    for i, (base_color, contrast_color) in enumerate(episodes):
        for repeat_count in range(10):
            print(f"[Experiment 4] Episode {i + 1}, Repetition {repeat_count + 1}/10")

            # Part 1: State 1 for 5s
            start_time = time.time()
            while time.time() - start_time < 5:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.VIDEORESIZE:
                        handle_resize(event)

                gradient_surface = generate_gradient_surface(base_color,
                                                             contrast_color,
                                                             progress=0.0)
                screen.blit(gradient_surface, (0, 0))
                pygame.display.flip()

            # Part 2: 1 -> 2 (3s)
            fade_duration = 3.0
            start_time = time.time()
            while time.time() - start_time < fade_duration:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.VIDEORESIZE:
                        handle_resize(event)

                elapsed = time.time() - start_time
                progress = elapsed / fade_duration
                gradient_surface = generate_gradient_surface(base_color,
                                                             contrast_color,
                                                             progress)
                screen.blit(gradient_surface, (0, 0))
                pygame.display.flip()

            # Part 3: 2 -> 1 (3s)
            start_time = time.time()
            while time.time() - start_time < fade_duration:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.VIDEORESIZE:
                        handle_resize(event)

                elapsed = time.time() - start_time
                progress = 1.0 - (elapsed / fade_duration)
                gradient_surface = generate_gradient_surface(base_color,
                                                             contrast_color,
                                                             progress)
                screen.blit(gradient_surface, (0, 0))
                pygame.display.flip()

        if i < len(episodes) - 1:
            next_episode_num = i + 2
            line1_text = f"Episode {i + 1} finished."
            line2_text = f"Press Space Key to Start Episode {next_episode_num}"
            show_text_screen(line1_text + '\n' + line2_text)

    if show_finish_screen:
        screen.fill(BLACK)
        finish_text_rect = finish_text.get_rect(
            center=(screen_width // 2, screen_height // 2)
        )
        screen.blit(finish_text, finish_text_rect)
        pygame.display.flip()
        wait_for_space()


def exp4_run_tutorial():
    show_text_screen(
        "This program measures pupil changes.\n"
        " Please make sure you have no eye diseases."
    )
    show_text_screen(
        "A gradient pattern will appear.\n"
        " It will fade in contrast and then fade back.\n"
        " Keep your eyes on the center cross."
    )

    base_color, contrast_color = EPISODES_EXP4[0]
    fade_duration = 3.0

    # 只做一次：5s state1 + 3s 1->2 + 3s 2->1
    start_time = time.time()
    while time.time() - start_time < 5:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                handle_resize(event)

        gradient_surface = generate_gradient_surface(base_color,
                                                     contrast_color,
                                                     progress=0.0)
        screen.blit(gradient_surface, (0, 0))
        pygame.display.flip()

    start_time = time.time()
    while time.time() - start_time < fade_duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                handle_resize(event)

        elapsed = time.time() - start_time
        progress = elapsed / fade_duration
        gradient_surface = generate_gradient_surface(base_color,
                                                     contrast_color,
                                                     progress)
        screen.blit(gradient_surface, (0, 0))
        pygame.display.flip()

    start_time = time.time()
    while time.time() - start_time < fade_duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                handle_resize(event)

        elapsed = time.time() - start_time
        progress = 1.0 - (elapsed / fade_duration)
        gradient_surface = generate_gradient_surface(base_color,
                                                     contrast_color,
                                                     progress)
        screen.blit(gradient_surface, (0, 0))
        pygame.display.flip()

    show_text_screen(
        "There are 5 color combinations in total. \n"
        " After one finish, press the space bar to proceed to the next combination. \n\n"
        " Time required for each combination: 50 seconds. \n"
        " Total time required: 4 minutes 20 seconds"
    )
    show_text_screen(
        "Tutorial complete. \n"
        " Press the spacebar to return to the main menu."
    )


# ===================== 顶层主菜单状态机 =====================

def main():
    state = "main_menu"

    while True:
        # 只在菜单状态中轮询事件；实验内部用自己的循环
        if state == "main_menu":
            labels = ["Experiment 1", "Experiment 2",
                      "Experiment 3", "Experiment 4", "Quit"]
            rects = get_main_menu_button_rects(labels)

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
                        state = "exp1_menu"
                    elif rects[1].collidepoint(event.pos):
                        state = "exp2_menu"
                    elif rects[2].collidepoint(event.pos):
                        state = "exp3_menu"
                    elif rects[3].collidepoint(event.pos):
                        state = "exp4_menu"
                    elif rects[4].collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

        # -------- Experiment 1 menu --------
        elif state == "exp1_menu":
            tutorial_button_rect, start_button_rect, back_button_rect = \
                get_three_button_rects()
            screen.fill(BLACK)
            draw_button(tutorial_button_rect, "Tutorial")
            draw_button(start_button_rect, "Start")
            draw_button(back_button_rect, "Back")
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    handle_resize(event)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if tutorial_button_rect.collidepoint(event.pos):
                        exp1_run_tutorial()
                    elif start_button_rect.collidepoint(event.pos):
                        exp1_run_experiment(episodes=EPISODES_EXP1)
                        # 实验结束后回主菜单（你的选项B）
                        state = "main_menu"
                    elif back_button_rect.collidepoint(event.pos):
                        state = "main_menu"

        # -------- Experiment 2 menu --------
        elif state == "exp2_menu":
            tutorial_button_rect, start_button_rect, back_button_rect = \
                get_three_button_rects()
            screen.fill(BLACK)
            draw_button(tutorial_button_rect, "Tutorial")
            draw_button(start_button_rect, "Start")
            draw_button(back_button_rect, "Back")
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    handle_resize(event)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if tutorial_button_rect.collidepoint(event.pos):
                        exp2_run_tutorial()
                    elif start_button_rect.collidepoint(event.pos):
                        exp2_run_experiment(episodes=EPISODES_EXP2)
                        state = "main_menu"
                    elif back_button_rect.collidepoint(event.pos):
                        state = "main_menu"

        # -------- Experiment 3 menu --------
        elif state == "exp3_menu":
            tutorial_button_rect, start_button_rect, back_button_rect = \
                get_three_button_rects()
            screen.fill(BLACK)
            draw_button(tutorial_button_rect, "Tutorial")
            draw_button(start_button_rect, "Start")
            draw_button(back_button_rect, "Back")
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    handle_resize(event)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if tutorial_button_rect.collidepoint(event.pos):
                        exp3_run_tutorial()
                    elif start_button_rect.collidepoint(event.pos):
                        exp3_run_new_experiment(episodes=EPISODES_EXP3)
                        state = "main_menu"
                    elif back_button_rect.collidepoint(event.pos):
                        state = "main_menu"

        # -------- Experiment 4 menu --------
        elif state == "exp4_menu":
            tutorial_button_rect, start_button_rect, back_button_rect = \
                get_three_button_rects()
            screen.fill(BLACK)
            draw_button(tutorial_button_rect, "Tutorial")
            draw_button(start_button_rect, "Start")
            draw_button(back_button_rect, "Back")
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    handle_resize(event)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if tutorial_button_rect.collidepoint(event.pos):
                        exp4_run_tutorial()
                    elif start_button_rect.collidepoint(event.pos):
                        exp4_run_gradient_experiment(episodes=EPISODES_EXP4)
                        state = "main_menu"
                    elif back_button_rect.collidepoint(event.pos):
                        state = "main_menu"


if __name__ == "__main__":
    main()

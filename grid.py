from LED import *
from random import randint
from math import sin

set_fps(80)
set_orientation(1)
set_window_scale(16)
W, H = get_width_adjusted(), get_height_adjusted()

G_SIZE = 2

snake_grid = [
    [randint(0, 3) for row in range(H // G_SIZE)] for column in range(W // G_SIZE + 1)
]

DIR = {"up": 0, "left": 1, "down": 2, "right": 3}

game_t = 0
game_speed = 3
snake = [(0, 0)]
dir_x, dir_y = 1, 0
fruit = None

snake_dir = DIR["right"]


def make_fruit():
    global fruit
    generate = True

    while generate:
        x = randint(0, W // G_SIZE - 1)
        y = randint(0, H // G_SIZE - 1)

        generate = (x, y) in snake

    fruit = (x, y)


make_fruit()

while True:
    game_t += 1
    head = snake[-1]

    # only want cardinal movement, no diagnols, so this is the cheaty way to do it
    if get_key("a") or get_key("d"):
        dir_y = 0
        dir_x = get_key("d") - get_key("a")
    elif get_key("w") or get_key("s"):
        dir_x = 0
        dir_y = get_key("s") - get_key("w")

    if game_t % game_speed == 0:
        new_head = head[0] + dir_x, head[1] + dir_y
        snake.append(new_head)

        if (new_head[0] == fruit[0] and new_head[1] == fruit[1]) or get_key("space"):
            make_fruit()
        else:
            snake = snake[1:]

    # draw background
    draw_offset = G_SIZE * 2

    for x in range(W):
        for y in range(H):
            my_grey = color_hsv(
                150, 100, 20 + (sin((game_t / 5 + x + y) / 20) ** 3) * 10
            )
            if (x + 2) % draw_offset == 0:
                draw_pixel(x, y, my_grey)

            if (y + 2) % draw_offset == 0:
                draw_pixel(x, y, my_grey)

            if ((x) % draw_offset == 0) and ((y) % draw_offset == 0):
                draw_pixel(x, y, my_grey)

    # draw snake 2
    # snake pos and then direction for line drawing
    # snake_segments = [
    #    (i, x1, y1, (x1 - x2), (y1 - y2))
    #    for i, ((x1, y1), (x2, y2)) in enumerate(
    #        zip([snake[0]] + snake[:-2], snake[:-1])
    #    )
    # ]

    # draw snake

    for layer in range(2):
        for i, ((x, y), (prev_x, prev_y)) in enumerate(
            zip([snake[0]] + snake[:-1], snake)
        ):
            x_off, y_off = x - prev_x, y - prev_y
            prev_x, prev_y = x, y

            x1, y1 = x * G_SIZE, y * G_SIZE
            x2, y2 = x1 - x_off, y1 - y_off

            for j, xx in enumerate(range(min(x1, x2), max(x1, x2) + 1)):
                for k, yy in enumerate(range(min(y1, y2), max(y1, y2) + 1)):
                    draw_pixel(
                        xx,
                        yy - layer,
                        color_hsv((i - j * x_off - k * y_off), 170, 100 + layer * 100),
                    )

    draw_pixel(
        fruit[0] * G_SIZE,
        fruit[1] * G_SIZE,
        color_hsv(150, 100, 200 + sin(game_t / 10) * 55),
    )

    draw()
    refresh()

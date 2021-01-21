import pygame
import random
from tkinter import messagebox as mb
from tkinter import Tk

pygame.init()

white = (255, 255, 255)  # цвета, которые будут использованы в дальнейшем
black = (0, 0, 0)
red = (200, 0, 0)
green = (0, 155, 0)
purple = (214, 32, 211)
blue = (0, 0, 255)

dark_blue_btn = (0, 128, 128)
light_blue_btn = (32, 178, 170)
dark_purple_btn = (199, 21, 133)
light_purple_btn = (255, 105, 180)
dark_yellow_btn = (200, 200, 0)
light_yellow_btn = (255, 255, 0)

light_red = (255, 0, 0)
light_blue = (28, 187, 187)

green_head = pygame.image.load('SnakeHeadGreen.png')  # спрайты
blue_head = pygame.image.load('SnakeHeadBlue.png')
purple_head = pygame.image.load('SnakeHeadPurple.png')

apple_img = pygame.image.load('apple.png')

font = pygame.font.SysFont("comicsansms", 50)  # шрифты
smallfont = pygame.font.SysFont("comicsansms", 25)
bigfont = pygame.font.SysFont("comicsansms", 85)

# создаём окно для игры
res_x = 600
res_y = 600
Display = pygame.display.set_mode((res_x, res_y))
FPS = 12
block_size = 20
apple_size = 32
apple_count = 1
col_volume = 0

pygame.display.set_caption("Super snake game")
pygame.display.set_icon(apple_img)
clock = pygame.time.Clock()

direction = "right"
apples = set([])


class Background(pygame.sprite.Sprite):  # класс, отвечающий за задний фон
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


BackGround1 = Background('grass.png', [0, 0])  # задний фон игры
BackGround = Background('back_snake.png', [0, 0])  # задний фон меню


class Snake:  # создание змейки
    def __init__(self, pos, vel, angle, image, color=green):
        self.pos = pos
        self.vel = vel
        self.angle = angle
        self.img = image
        self.list = []
        self.lenght = 1
        self.head = self.img
        self.color = color

    def score_display(self, pos):
        score(self.lenght - 1, pos, self.color)

    def key_event(self, direction_):
        self.angle = direction_

    def eat(self):  # алгоритм для отслеживания, поймала ли змея яблоко или нет
        for apple in apples:
            if self.pos[0] > apple.pos[0] and self.pos[0] < apple.pos[0] + apple_size or \
                    self.pos[0] + block_size > apple.pos[0] and self.pos[0] < apple.pos[0] + apple_size:
                if self.pos[1] > apple.pos[1] and self.pos[1] < apple.pos[1] + apple.size \
                        or self.pos[1] + block_size > apple.pos[1] and self.pos[1] < apple.pos[1] + apple.size:
                    apples.remove(apple)
                    apples.add(apple_spawn())
                    self.lenght += 1

    def update(self):
        gameOver = False

        if (self.angle == "right") and (self.vel[0] != -block_size):
            self.vel[0] = +block_size
            self.vel[1] = 0
            self.head = pygame.transform.rotate(self.img, 270)

        if (self.angle == "left") and (self.vel[0] != block_size):
            self.vel[0] = -block_size
            self.vel[1] = 0
            self.head = pygame.transform.rotate(self.img, 90)

        if (self.angle == "up") and (self.vel[1] != block_size):
            self.head = self.img
            self.vel[1] = -block_size
            self.vel[0] = 0

        if (self.angle == "down") and (self.vel[1] != -block_size):
            self.vel[1] = +block_size
            self.vel[0] = 0
            self.head = pygame.transform.rotate(self.img, 180)

        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        # "строим" нашу змейку
        snakeHead = []
        snakeHead.append(self.pos[0])
        snakeHead.append(self.pos[1])
        self.list.append(snakeHead)
        if len(self.list) > self.lenght:
            del self.list[0]
        if snakeHead in self.list[:-1]:
            gameOver = True
        # рисуем туловище змеи
        for XnY in self.list[:-1]:
            pygame.draw.rect(Display, self.color, [XnY[0], XnY[1], block_size, block_size])
        # рисуем голову змеи
        Display.blit(self.head, (self.list[-1][0], self.list[-1][1]))

        # проверяем условия, при которых игрок может проиграть
        if self.pos[0] < 0 or self.pos[0] >= res_x or self.pos[1] < 0 or self.pos[1] >= res_y:
            gameOver = True
        return gameOver


class Apple:  # создание яблока
    def __init__(self, pos, size, image=None):
        self.pos = pos
        self.img = image
        self.size = size

    def draw(self):
        Display.blit(self.img, self.pos)


def pause():
    paused = True
    message_screen("Пауза", black, -100, "large")
    message_screen("Нажми SPACE, чтобы продолжить", black, 25)
    message_screen("Нажми HOME, чтобы попасть в меню", black, 55)

    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                check_quit('ToExit')
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False
                if event.key == pygame.K_ESCAPE:
                    check_quit('ToExit')
                if event.key == pygame.K_HOME:
                    check_quit('ToMenu')

        clock.tick(10)


def check_quit(option):  # диалоговое окно, которое узнаёт, хочет ли игрок выйти
    root = Tk()
    root.withdraw()
    if option == 'ToMenu':
        msg = 'Вы уверены, что хотите перейти в меню?'
    elif option == 'ToExit':
        msg = 'Вы уверены, что хотите выйти из игры?'
    answer = mb.askyesno(title="Super snake game",
                         message=msg)
    if answer is True and option == 'ToExit':
        pygame.quit()
        quit()
    elif option == 'ToMenu' and answer is True:
        game_intro()


def score(scr, pos, color):  # отображение очков
    text = smallfont.render("Очки: " + str(scr), True, color)
    Display.blit(text, pos)


def text_objects(text, color, size="small"):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = font.render(text, True, color)
    elif size == "large":
        textSurface = bigfont.render(text, True, color)
    return textSurface, textSurface.get_rect()


def text_to_button(msg, color, pos, size="small"):
    text_surf, text_rect = text_objects(msg, color, size)
    text_rect.center = (pos[0] + (pos[2] / 2), pos[1] + (pos[3] / 2))
    Display.blit(text_surf, text_rect)


def message_screen(msg, color, y_displace=0, size="small"):
    text_surf, text_rect = text_objects(msg, color, size)
    text_rect.center = (res_x / 2), (res_y / 2) + y_displace
    Display.blit(text_surf, text_rect)


def apple_spawn():
    new_apple = Apple([round(random.randrange(apple_size, res_x - apple_size) / 10) * 10,
                       round(random.randrange(apple_size, res_y - apple_size) / 10) * 10],
                      apple_size, apple_img)
    return new_apple


def game_controls():  # инструкция управления
    global col_volume
    controlls = True

    Display.blit(BackGround.image, BackGround.rect)
    message_screen("Управление", white, -120, "large")
    message_screen('Зелёная змея: стрелки "вниз",', (240, 255, 255), -30, "small")
    message_screen('"вверх", "влево", вправо"', (240, 255, 255), 0, "small")

    message_screen("Розовая змея: кнопки W, D, S, A", (255, 228, 225), 40, "small")
    message_screen("Пауза: P", white, 70, "small")
    message_screen("Включить/выключить звук: V", white, 100, "small")

    while controlls:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                check_quit('ToExit')
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    controlls = False
                if event.key == pygame.K_ESCAPE:
                    check_quit('ToExit')
                if event.key == pygame.K_HOME:
                    game_intro()
                if event.key == pygame.K_v:
                    col_volume += 1
                    pygame.mixer.music.set_volume(0)
                    if col_volume % 2 == 0:
                        pygame.mixer.music.set_volume(1)

        controlls = button("Меню", (res_x / 2 - 80, res_y - 150, 160, 50), dark_yellow_btn, light_yellow_btn,
                           action="switch")

        clock.tick(30)
        pygame.display.update()


def button(text, pos, color1, color2, action, text_color=black):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if pos[0] + pos[2] > cur[0] > pos[0] and pos[1] + pos[3] > cur[1] > pos[1]:
        pygame.draw.rect(Display, color2, pos)
        if click[0] == 1:
            if action == "one_player":
                game_oneplayer()
            elif action == "controls":

                clock.tick(6)
                game_controls()
                clock.tick(6)
            elif action == "two_players":
                game_twoplayers()
            elif action == 'switch':
                return False
    else:
        pygame.draw.rect(Display, color1, pos)
    text_to_button(text, text_color, pos)

    return True


def game_intro():  # меню
    global col_volume
    intro = True

    pygame.mixer.music.load('theme_music.mp3')
    pygame.mixer.music.play(-1)
    # отключение звука
    if col_volume % 2 == 0:
        pygame.mixer.music.set_volume(1)
    else:
        pygame.mixer.music.set_volume(0)

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                check_quit('ToExit')
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False
                if event.key == pygame.K_ESCAPE:
                    check_quit('ToExit')
                if event.key == pygame.K_v:
                    col_volume += 1
                    pygame.mixer.music.set_volume(0)
                    if col_volume % 2 == 0:
                        pygame.mixer.music.set_volume(1)

        Display.blit(BackGround.image, BackGround.rect)
        message_screen("Супер змейка", white, -120, "large")
        message_screen("Собери все яблоки", white, -30, "small")
        intro = button("Одиночная игра", (res_x / 2 - 290, res_y - 150, 205, 50), dark_blue_btn, light_blue_btn,
                       action="one_player")
        button("Управление", (res_x / 2 - 80, res_y - 150, 175, 50), dark_yellow_btn, light_yellow_btn,
               action="controls")
        button("Игра с другом", (res_x / 2 + 100, res_y - 150, 190, 50), dark_purple_btn, light_purple_btn,
               action="two_players")
        clock.tick(30)
        pygame.display.update()


def game_twoplayers():  # функция, отвечающая за игру для двух игроков
    global apple_count, col_volume

    # отключение звука
    if col_volume % 2 == 0:
        pygame.mixer.music.set_volume(1)
    else:
        pygame.mixer.music.set_volume(0)

    pygame.mixer.music.load('theme_music.mp3')
    pygame.mixer.music.play(-1)
    gameExit = False
    gameOver = False

    while apple_count > len(apples):
        apple = apple_spawn()
        apples.add(apple)

    snake1 = Snake([((res_x / 2 - 5 * block_size) / 10) * 10, (res_y / 20) * 10], [0, 0], None, green_head)
    snake2 = Snake([((res_x / 2 - 5 * block_size) / 10) * 10, (res_y / 20) * 10], [0, 0], None, purple_head, purple)

    while not gameExit:
        if apple_count > len(apples):
            apple = apple_spawn()
            apples.add(apple)
        elif apple_count < len(apples):
            apples.pop()

        if gameOver is True:
            pygame.mixer.music.stop()
            pygame.mixer.music.load('die_music.mp3')
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(1)

            message_screen("Игра окончена!", red, -50, "medium")
            message_screen("Нажми SPACE, чтобы продолжить", black, 30)
            message_screen("Нажми ESC, чтобы выйти", black, 60)
            message_screen("Нажми HOME, чтобы попасть в меню", black, 90)

            pygame.display.update()
            while gameOver is True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        check_quit('ToExit')
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            check_quit('ToExit')
                        if event.key == pygame.K_SPACE:
                            game_twoplayers()
                        if event.key == pygame.K_HOME:
                            pygame.mixer.music.stop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
                check_quit('ToExit')
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  # Snake1
                    snake1.key_event("left")

                if event.key == pygame.K_RIGHT:
                    snake1.key_event("right")

                if event.key == pygame.K_DOWN:
                    snake1.key_event("down")

                if event.key == pygame.K_UP:
                    snake1.key_event("up")

                if event.key == pygame.K_a:  # Snake2
                    snake2.key_event("left")

                if event.key == pygame.K_d:
                    snake2.key_event("right")

                if event.key == pygame.K_s:
                    snake2.key_event("down")

                if event.key == pygame.K_w:
                    snake2.key_event("up")

                if event.key == pygame.K_SPACE:
                    pause()
                if event.key == pygame.K_ESCAPE:
                    check_quit('ToExit')
                    pause()
                    gameExit = False
                if event.key == pygame.K_p:
                    pause()
                if event.key == pygame.K_e:
                    apple_count += 1
                if event.key == pygame.K_q:
                    apple_count = 100
                if event.key == pygame.K_HOME:
                    check_quit('ToMenu')
                    pause()

                if event.key == pygame.K_v:  # звук
                    col_volume += 1
                    pygame.mixer.music.set_volume(0)
                    if col_volume % 2 == 0:
                        pygame.mixer.music.set_volume(1)

        Display.blit(BackGround1.image, BackGround1.rect)  # задний фон

        for apple in apples:
            apple.draw()

        if snake1.update() or snake2.update():
            gameOver = True

        snake1.score_display([50, 2])
        snake1.eat()
        snake2.score_display([res_x - 150, 2])
        snake2.eat()

        pygame.display.update()

        clock.tick(FPS)
    exit_game()


def game_oneplayer():  # функция для создания одиночной игры
    global apple_count, col_volume

    # отключение звука
    if col_volume % 2 == 0:
        pygame.mixer.music.set_volume(1)
    else:
        pygame.mixer.music.set_volume(0)

    pygame.mixer.music.load('theme_music.mp3')
    pygame.mixer.music.play(-1)
    gameExit = False
    gameOver = False
    while apple_count > len(apples):
        apple = apple_spawn()
        apples.add(apple)
    snake = Snake([((res_x / 2 - 5 * block_size) / 10) * 10, (res_y / 20) * 10], [0, 0], None, blue_head, light_blue)

    while not gameExit:
        if apple_count > len(apples):
            apple = apple_spawn()
            apples.add(apple)
        elif apple_count < len(apples):
            apples.pop()

        if gameOver is True:
            pygame.mixer.music.stop()
            pygame.mixer.music.load('die_music.mp3')
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play()

            message_screen("Игра окончена!", red, -50, "medium")
            message_screen("Нажми SPACE, чтобы продолжить", black, 30)
            message_screen("Нажми ESC, чтобы выйти", black, 60)
            message_screen("Нажми HOME, чтобы попасть в меню", black, 90)

            pygame.display.update()
            while gameOver is True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        check_quit('ToExit')
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            check_quit('ToExit')
                        if event.key == pygame.K_SPACE:
                            game_oneplayer()

                        if event.key == pygame.K_HOME:
                            pygame.mixer.music.stop()
                            game_intro()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
                check_quit('ToExit')
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  # Snake
                    snake.key_event("left")

                if event.key == pygame.K_RIGHT:
                    snake.key_event("right")

                if event.key == pygame.K_DOWN:
                    snake.key_event("down")

                if event.key == pygame.K_UP:
                    snake.key_event("up")

                if event.key == pygame.K_SPACE:
                    pause()
                if event.key == pygame.K_ESCAPE:
                    gameExit = True
                if event.key == pygame.K_p:
                    pause()
                if event.key == pygame.K_e:
                    apple_count += 1
                if event.key == pygame.K_q:
                    apple_count = 100
                if event.key == pygame.K_HOME:
                    check_quit('ToMenu')
                    pause()
                if event.key == pygame.K_v:  # звук
                    col_volume += 1
                    pygame.mixer.music.set_volume(0)
                    if col_volume % 2 == 0:
                        pygame.mixer.music.set_volume(1)

        Display.blit(BackGround1.image, BackGround1.rect)

        for apple in apples:
            apple.draw()

        if snake.update():
            gameOver = True

        snake.score_display([50, 2])
        snake.eat()

        pygame.display.update()

        clock.tick(FPS)
    exit_game()


def exit_game():
    pygame.quit()
    quit()


game_intro()

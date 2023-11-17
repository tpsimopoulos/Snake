import pygame
import random

pygame.init()
pygame.mixer.init()

FPS = 30
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
clock = pygame.time.Clock()
pygame.display.set_caption('Snake')
size = screen_width, screen_height = 350, 350
screen = pygame.display.set_mode(size)
eat_sound = pygame.mixer.Sound("/Users/tpsimopoulos/PythonProjects/Snake/Snake/power_up.wav")


def show_go_screen():
    screen.fill((0, 0, 0))
    draw_text(screen, "Snake", 50, screen_width / 2, screen_height * .2)
    draw_text(screen, "Press Any Key To Start", 30, screen_width / 2, screen_height / 3)
    pygame.display.flip()

    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                waiting = False


def draw_text(surface, text, text_size, x, y):
    font = pygame.font.Font('freesansbold.ttf', text_size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)


class Player:
    game_speed = 5

    def __init__(self):
        self.x = screen_width / 2
        self.y = screen_height / 2
        self.width = 15
        self.height = 15
        self.x_speed = Player.game_speed
        self.y_speed = 0
        self.head = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw_player(self, surface):
        # Drawing head of snake
        pygame.draw.rect(surface, GREEN, self.head)

    def our_snake(self, body_list):
        for x in body_list:
            pygame.draw.rect(screen, GREEN, [x[0], x[1], self.width, self.width])

    def snake_ate(self, food):
        if self.head.colliderect(food):
            return True

    def out_of_bounds(self):
        # Collision with the boundaries
        if self.head.y < 0 or self.head.y > screen_height - self.height or \
                self.head.x < 0 or self.head.x > screen_width - self.width:
            return True


class Food:
    def __init__(self):
        self.width = 10
        self.height = 10
        self.x = round(random.randint(0, screen_width-self.width)/10)*10
        self.y = round(random.randint(0, screen_height-self.height)/10)*10
        self.color = RED
        self.food = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw_food(self, surface):
        pygame.draw.rect(surface, self.color, self.food)


game_over = True
running = True
while running:

    clock.tick(FPS)

    while game_over:
        show_go_screen()
        score = 0
        f = Food()
        p = Player()
        snake_list = []
        snake_length = 1
        game_over = False

    # Process input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        p.x_speed = -Player.game_speed
        p.y_speed = 0
    if keys[pygame.K_RIGHT]:
        p.x_speed = Player.game_speed
        p.y_speed = 0
    if keys[pygame.K_UP]:
        p.y_speed = -Player.game_speed
        p.x_speed = 0
    if keys[pygame.K_DOWN]:
        p.y_speed = Player.game_speed
        p.x_speed = 0

    # Update
    p.head.move_ip(p.x_speed, p.y_speed)

    snake_head = [p.head.x, p.head.y]
    snake_list.append(snake_head)
    if len(snake_list) > snake_length:
        del snake_list[0]

    for segment in snake_list[:-1]:
        if segment == snake_head:
            game_over = True

    if p.out_of_bounds():
        game_over = True

    if p.snake_ate(f.food):
        eat_sound.play()
        f = Food()
        score += 1
        snake_length += 1

    # Draw
    screen.fill((0, 0, 0))
    p.draw_player(screen)
    f.draw_food(screen)
    p.our_snake(snake_list)
    draw_text(screen, str(score), 18, screen_width / 2, 10)
    pygame.display.flip()

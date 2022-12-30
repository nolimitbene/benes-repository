import pygame, random
pygame.init()

# Constant variables
WIDTH, HEIGHT = 800, 620
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption("Dodging Falling Things Game")
WHITE = (225,225,225)
BLACK = (0,0,0)
GREY = (192,192,192)
RED = (128,0,0)
BRIGHT_RED = (225,6,0)
GREEN = (0,225,0)
YELLOW = (225,225,0)
FPS = 60
GROUND_HEIGHT = 90
PLAYER_HEIGHT, PLAYER_WIDTH = 50, 55
OBSTACLE_HEIGHT, OBSTACLE_WIDTH = 50, 50
SPEEDUP_HEIGHT, SPEEDUP_WIDTH = 40, 40
HEALTHUP_HEIGHT, HEALTHUP_WIDTH = 45, 45
WINNING_ROUNDS = 50
FONT = pygame.font.SysFont('comicsans', 50)
lose_text = 'YOU LOSE!'
win_text = 'YOU WIN!'


# Player
class Player:
    COLOUR = WHITE
    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = y
        self.width = width
        self.height = height
        self.VEL = self.original_VEL = 5
        self.health = self.original_health = 3

    def draw(self, win):
        pygame.draw.rect(win, self.COLOUR, (self.x, self.y, self.width, self.height))

    def reset(self):
        self.x = self.original_x
        self.health = self.original_health
        self.VEL = self.original_VEL


# Falling obsticle
class Obstacle:
    COLOUR = BRIGHT_RED
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height
        self.VEL = 7
        self.rounds = self.original_rounds = 0

    def draw(self, win):
        pygame.draw.rect(win, self.COLOUR, (self.x, self.y, self.width, self.height))

    def move(self):
        self.y += self.VEL

    def reset(self):
        self.y = self.original_y
        self.x = random.randint(0, WIDTH - OBSTACLE_WIDTH)
        
    def reset_score(self):
        self.rounds = 0


class SpeedPowerUp(Obstacle):
    COLOUR = YELLOW


class HealthPowerUp(Obstacle):
    COLOUR = GREEN


class Ground:
    COLOUR = BLACK
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOUR, (self.x, self.y, self.width, self.height))


# Draws objects to window
def draw_win(win, player, obstacle, obstacle1, obstacle2, obstacle3, obstacle4, ground, speedup, healthup):
    win.fill(RED)

    player.draw(WIN)
    ground.draw(WIN)
    obstacle.draw(WIN)
    obstacle1.draw(WIN)
    obstacle2.draw(WIN)
    obstacle3.draw(WIN)
    obstacle4.draw(WIN)
    speedup.draw(WIN)
    healthup.draw(WIN)

    obstacle.move()
    obstacle1.move()
    obstacle2.move()
    obstacle3.move()
    obstacle4.move()
    speedup.move()
    healthup.move()

    pygame.display.update()


# User keyboard input movement (left, right)
def handle_player_movement(keys, player):
    if keys[pygame.K_RIGHT] and player.x + PLAYER_WIDTH < WIDTH:
        player.x += player.VEL
    elif keys[pygame.K_LEFT] and player.x > 0:
        player.x -= player.VEL


def handle_obstacle_player_collision(obstacle, player):
    hit_popup = 'HIT!'
    lives_counter = f'Lives: {player.health}'
    lives_text = FONT.render(lives_counter, 1, WHITE)
    hit_text = FONT.render(hit_popup, 1, WHITE)
    WIN.blit(lives_text, (12, 12))
    pygame.display.update()

    # If player hit
    if obstacle.y + OBSTACLE_HEIGHT >= player.y and obstacle.x + OBSTACLE_WIDTH >= player.x and obstacle.x < player.x + PLAYER_WIDTH:
        obstacle.reset()
        player.health -= 1
        player.VEL -= 0.5

        if player.health > 0:
            WIN.blit(hit_text, (WIDTH//2 - hit_text.get_width()//2, HEIGHT//2 - hit_text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(250)


def handle_speedup_player_collision(player, speedup):
    speed_text = 'PLAYER SPEED INCREASED'
    text = FONT.render(speed_text, 1, WHITE)
    if speedup.y + SPEEDUP_HEIGHT >= player.y and speedup.x + SPEEDUP_WIDTH >= player.x and speedup.x < player.x + PLAYER_WIDTH:
        speedup.reset()
        player.VEL += 1

        WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
        pygame.display.update()
        pygame.time.delay(450)


def handle_healthup_player_collision(player, healthup):
    health_text = '+1 LIFE'
    text = FONT.render(health_text, 1, WHITE)
    if healthup.y + HEALTHUP_HEIGHT >= player.y and healthup.x + HEALTHUP_WIDTH >= player.x and healthup.x < player.x + PLAYER_WIDTH:
        healthup.reset()
        player.health += 1

        WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
        pygame.display.update()
        pygame.time.delay(400)



def handle_obstacle_ground_collision(obstacle, ground, speedup, healthup):
    if obstacle.y + OBSTACLE_HEIGHT >= ground.y:
            obstacle.reset()
            obstacle.rounds += 1
    elif speedup.y + SPEEDUP_HEIGHT >= ground.y:
            speedup.reset()
    elif healthup.y + HEALTHUP_HEIGHT >= ground.y:
            healthup.reset()


def all_obstacles_reset(obstacle, obstacle1, obstacle2, obstacle3, obstacle4):
    obstacle.reset()
    obstacle1.reset()
    obstacle2.reset()
    obstacle3.reset()
    obstacle4.reset()


def main():
    clock = pygame.time.Clock()

    # Obstacle appears at random x coordiante at the top of the window
    obstacle = Obstacle(random.randint(0, WIDTH - OBSTACLE_WIDTH), 0, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
    obstacle1 = Obstacle(random.randint(0, WIDTH - OBSTACLE_WIDTH), -45, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
    obstacle2 = Obstacle(random.randint(0, WIDTH - OBSTACLE_WIDTH), -90, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
    obstacle3 = Obstacle(random.randint(0, WIDTH - OBSTACLE_WIDTH), -140, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
    obstacle4 = Obstacle(random.randint(0, WIDTH - OBSTACLE_WIDTH), -195, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
    player = Player(WIDTH//2, HEIGHT - GROUND_HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    speedup = SpeedPowerUp(random.randint(0, WIDTH - OBSTACLE_WIDTH), -2500, SPEEDUP_WIDTH, SPEEDUP_HEIGHT)
    healthup = HealthPowerUp(random.randint(0, WIDTH - OBSTACLE_WIDTH), -1500, SPEEDUP_WIDTH, SPEEDUP_HEIGHT)
    ground = Ground(0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT)

    game_loop = True
    while game_loop:
        clock.tick(FPS)
        draw_win(WIN, player, obstacle, obstacle1, obstacle2, obstacle3, obstacle4, ground, speedup, healthup)
        keys = pygame.key.get_pressed()

        # if user Xes out of window, game loop stops
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_loop = False

        handle_player_movement(keys, player)

        handle_obstacle_player_collision(obstacle, player)
        handle_obstacle_player_collision(obstacle1, player)
        handle_obstacle_player_collision(obstacle2, player)
        handle_obstacle_player_collision(obstacle3, player)
        handle_obstacle_player_collision(obstacle4, player)

        handle_speedup_player_collision(player, speedup)

        handle_healthup_player_collision(player, healthup)

        handle_obstacle_ground_collision(obstacle, ground, speedup, healthup)
        handle_obstacle_ground_collision(obstacle1, ground, speedup, healthup)
        handle_obstacle_ground_collision(obstacle2, ground, speedup, healthup)
        handle_obstacle_ground_collision(obstacle3, ground, speedup, healthup)
        handle_obstacle_ground_collision(obstacle4, ground, speedup, healthup)

        # Player loses if health is less than 0
        if player.health <= 0:
            text = FONT.render(lose_text, 1, WHITE)
            WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(3000)
            player.reset()
            all_obstacles_reset(obstacle, obstacle1, obstacle2, obstacle3, obstacle4)
            obstacle.reset_score()

        # Player wins if they survive certain amount of rounds
        if obstacle.rounds >= WINNING_ROUNDS:
            text = FONT.render(win_text, 1, WHITE)
            WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(3000)
            player.reset()
            all_obstacles_reset(obstacle, obstacle1, obstacle2, obstacle3, obstacle4)
            obstacle.reset_score()
        
    pygame.quit()

main()

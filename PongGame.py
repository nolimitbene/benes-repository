import pygame as pyg
pyg.init()

# Window/Display
pyg.display.set_caption('Pong Game')
WIN_WIDTH, WIN_HEIGHT = 800, 620
WIN = pyg.display.set_mode((WIN_WIDTH, WIN_HEIGHT)) 

# CONSTANT variables
WHITE = (225, 225, 225)
BLACK = (0, 0, 0)
FPS = 60
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
BALL_RADIUS = 9

SCORE_FONT = pyg.font.SysFont('comicsans', 50) 
WINNING_SCORE = 10

class Ball:
    MAX_VEL = 6
    COLOUR = WHITE
    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pyg.draw.circle(win, self.COLOUR,(self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1


class Paddle:
    COLOUR = WHITE
    VEL = 4
    def __init__(self, x, y, width, height):
        self.x = self.original_x =x
        self.y = self.original_y =y 
        self.width = width
        self.height = height

    def draw(self, win):
        pyg.draw.rect(win, self.COLOUR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y


# Draws window
def draw_win(win, paddles, ball, left_score, right_score):
    win.fill(BLACK)

    left_score_text = SCORE_FONT.render(f'{left_score}', 1, WHITE)
    right_score_text = SCORE_FONT.render(f'{right_score}', 1, WHITE)
    win.blit(left_score_text, (WIN_WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (WIN_WIDTH * (3/4) - right_score_text.get_width()//2, 20))

    for paddle in paddles:
        paddle.draw(win)

    for i in range(10, WIN_HEIGHT, WIN_HEIGHT//20):
        if i % 2 == 1:
            continue
        else:
            pyg.draw.rect(win, WHITE, (WIN_WIDTH//2 - 5, i, 10, WIN_HEIGHT//20))

    ball.draw(win)

    pyg.display.update()


def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= WIN_HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    # left paddle collision
    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

    # right paddle collision
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel


def handle_paddle_movement(keys, left_paddle, right_paddle):

    # left paddle movement
    if keys[pyg.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    if keys[pyg.K_s] and left_paddle.y + left_paddle.height + left_paddle.VEL <= WIN_HEIGHT:
        left_paddle.move(up=False)

    # right paddle movement
    if keys[pyg.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pyg.K_DOWN] and right_paddle.y + right_paddle.height + left_paddle.VEL <= WIN_HEIGHT:
        right_paddle.move(up=False)

def main():
    clock = pyg.time.Clock()
    game_loop = True
    left_paddle = Paddle(10, WIN_HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIN_WIDTH - 10 - PADDLE_WIDTH, WIN_HEIGHT//2 - PADDLE_HEIGHT//2,PADDLE_WIDTH, PADDLE_HEIGHT)

    ball = Ball(WIN_WIDTH//2, WIN_HEIGHT//2, BALL_RADIUS)

    left_score = 0
    right_score = 0

    while game_loop:
        clock.tick(FPS)
        draw_win(WIN, [left_paddle, right_paddle], ball, left_score, right_score)

        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                game_loop = False 

        keys = pyg.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)
        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        won = False

        if ball.x < 0:
            right_score += 1
            ball.reset()

        elif ball.x > WIN_WIDTH:
            left_score += 1
            ball.reset()

        if left_score >= WINNING_SCORE:
            won = True
            win_text = 'Left Player Wins!'
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = 'Right Player Wins!'

        if won:
            text = SCORE_FONT.render(win_text, 1, WHITE)
            WIN.blit(text, (WIN_WIDTH//2 - text.get_width()//2, WIN_HEIGHT//2 - text.get_height()//2))
            pyg.display.update()
            pyg.time.delay(3500)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0

    pyg.quit()

main()

# pong
import random
import pygame
import sys
from pygame import *

WIDTH = 400
HEIGHT = 300
LINE = 10
PAD_SIZE = 50
PAD_DIS = 20

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def drawArena():
    SCREEN.fill(BLACK)
    pygame.draw.rect(SCREEN, WHITE, ((0,0),(WIDTH, HEIGHT)), LINE * 2)
    pygame.draw.line(SCREEN, WHITE, ((WIDTH // 2), 0), ((WIDTH // 2), HEIGHT), (LINE // 4))

def drawPaddle(paddle):
    if paddle.bottom > HEIGHT - LINE:
        paddle.bottom = HEIGHT - LINE
    elif paddle.top < LINE:
        paddle.top = LINE
    pygame.draw.rect(SCREEN, WHITE, paddle)

def drawBall(ball):
    pygame.draw.rect(SCREEN, WHITE, ball)

def moveBall(ball, ballDirX, ballDirY):
    ball.x += ballDirX
    ball.y += ballDirY
    return ball

def wallBounce(ball, ballDirX, ballDirY):
    if ball.top == (LINE) or ball.bottom == (HEIGHT - LINE):
        ballDirY = ballDirY * -1
    if ball.left == (LINE) or ball.right == (WIDTH - LINE):
        ballDirX = ballDirX * -1
    return ballDirX, ballDirY

def hitBall(ball, paddle1, paddle2, ballDirX):
    if ballDirX == -1 and paddle1.right == ball.left and paddle1.top < ball.top and paddle1.bottom > ball.bottom:
        return -1
    elif ballDirX == 1 and paddle2.left == ball.right and paddle2.top < ball.top and paddle2.bottom > ball.bottom:
        return -1
    else: return 1

def paddleMove(ball, ballDirX, paddle2):
    if ballDirX == -1:
        if paddle2.centery < (HEIGHT // 2):
            paddle2.y += 1
        elif paddle2.centery > (HEIGHT // 2):
            paddle2.y -= 1
    elif ballDirX == 1:
        if paddle2.centery < ball.centery:
            paddle2.y += 1
        else:
            paddle2.y -= 1
    return paddle2

def main():
    pygame.init()
    global SCREEN

    fps = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Test Pong')

    ballX = WIDTH // 2 - LINE // 2
    ballY = HEIGHT // 2 - LINE // 2
    playerOnePosition = (HEIGHT - PAD_SIZE) // 2
    playerTwoPosition = (HEIGHT - PAD_SIZE) // 2

    ballDirX = -1
    ballDirY = -1

    paddle1 = pygame.Rect(PAD_DIS, playerOnePosition, LINE, PAD_SIZE)
    paddle2 = pygame.Rect(WIDTH - PAD_DIS - LINE, playerTwoPosition, LINE, PAD_SIZE)
    ball = pygame.Rect(ballX, ballY, LINE, LINE)

    drawArena()
    drawPaddle(paddle1)
    drawPaddle(paddle2)
    drawBall(ball)

    pygame.mouse.set_visible(0)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                paddle1.y = mousey

        drawArena()
        drawPaddle(paddle1)
        drawPaddle(paddle2)
        drawBall(ball)

        ball = moveBall(ball, ballDirX, ballDirY)
        ballDirX, ballDirY = wallBounce(ball, ballDirX, ballDirY)
        ballDirX = ballDirX * hitBall(ball, paddle1, paddle2, ballDirX)
        paddle2 = paddleMove(ball, ballDirX, paddle2)

        pygame.display.update()
        fps.tick(60)

main()

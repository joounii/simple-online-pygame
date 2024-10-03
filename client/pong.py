import pygame
import queue
import sys
import json
import socket
import threading
from colored_print import log

position_str_l = "0,0"
position_str_r = "0,0"

def send_paddle_pos(paddle, client_socket, is_left):
    global position_str_l
    global position_str_r
    if(is_left == True):
        if(position_str_l != f"{paddle[0]},{paddle[1]}"):
            position_str_l = f"{paddle[0]},{paddle[1]}"
            message = {"command": "almost_all", "message": position_str_l}
            client_socket.send(json.dumps(message).encode('utf-8'))
    else:
        if(position_str_r != f"{paddle[0]},{paddle[1]}"):
            position_str_r = f"{paddle[0]},{paddle[1]}"
            message = {"command": "almost_all", "message": position_str_r}
            client_socket.send(json.dumps(message).encode('utf-8'))
    
    

def game(client_socket, message_queue):
    global position_str_l
    
    # Initialize pygame
    pygame.init()

    # Define screen dimensions and colors
    WIDTH, HEIGHT = 800, 600
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Create the screen object
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Pong')

    # Define paddles and ball
    paddle_width, paddle_height = 10, 100
    ball_size = 20
    paddle_speed = 6
    ball_speed_x, ball_speed_y = 5, 5

    # Paddle positions
    left_paddle = pygame.Rect(30, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)
    right_paddle = pygame.Rect(WIDTH - 40, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)

    # Ball position and velocity
    ball = pygame.Rect(WIDTH // 2 - ball_size // 2, HEIGHT // 2 - ball_size // 2, ball_size, ball_size)

    # Game loop
    while True:
        message = ""
        received_message = False
        try:
            message = message_queue.get_nowait()
            log.warning(message)
            received_message = True
        except queue.Empty:
            received_message = False
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Key inputs for paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and left_paddle.top > 0:
            left_paddle.y -= paddle_speed
        if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
            left_paddle.y += paddle_speed
        if keys[pygame.K_UP] and right_paddle.top > 0:
            right_paddle.y -= paddle_speed
        if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
            right_paddle.y += paddle_speed

        # Ball movement
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Ball collision with top and bottom walls
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y = -ball_speed_y

        # Ball collision with paddles
        if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
            ball_speed_x = -ball_speed_x

        # Ball goes out of bounds (reset to the center)
        if ball.left <= 0 or ball.right >= WIDTH:
            ball.x = WIDTH // 2 - ball_size // 2
            ball.y = HEIGHT // 2 - ball_size // 2
            ball_speed_x = -ball_speed_x

        # Fill the screen with black color
        screen.fill(BLACK)

        # Draw paddles and ball
        # if(position_str != f"{left_paddle[0]},{left_paddle[1]}"):
        #     position_str = f"{left_paddle[0]},{left_paddle[1]}"
        #     client_socket.send(position_str.encode('utf-8'))
        
        send_paddle_pos(left_paddle, client_socket, True)
        
        pygame.draw.rect(screen, WHITE, left_paddle)
        pygame.draw.rect(screen, WHITE, right_paddle)
        pygame.draw.ellipse(screen, WHITE, ball)

        # Draw center line
        pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        # Update the display
        pygame.display.flip()

        # Set the frame rate
        pygame.time.Clock().tick(60)
        if(received_message):
            message_queue.task_done()

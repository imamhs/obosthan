# Copyright (c) 2019, Md Imam Hossain (emamhd at gmail dot com)
# see LICENSE.txt for details

import pygame
import obosthan

frame_count = 0
FRAMES_PER_SECOND = 25
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Obosthan point example')
pygame.key.set_repeat(1, 10)
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 50)
font = pygame.font.Font(None, 24)

x = y = 200
move_left = False

c1 = obosthan.OPoint2D(x, y)
c2 = obosthan.OPoint2D(x+100, y+100)

done = False
pause = False

while not done:
    for event in pygame.event.get():

        if event.type == pygame.USEREVENT:

            if move_left == False:
                c1[0] = c1[0] + 5
            else:
                c1[0] = c1[0] - 5

            if c1[0] > SCREEN_WIDTH - 200:
                move_left = True
            if c1[0] <  200:
                move_left = False

        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if pause == False:
                    pause = True
                else:
                    pause = False

        c2[0] = pygame.mouse.get_pos()[0]
        c2[1] = pygame.mouse.get_pos()[1]

    if pause == False:

        frame_count = frame_count + 1
        text_frame_count = font.render('Frame count ' + str(frame_count), True, (255, 255, 255))
        text_distance = font.render('Distance ' + str(round(c1.distance_to(c2),2)), True, (255, 255, 255))
        screen.fill((0, 0, 0))
        screen.blit(text_frame_count, (SCREEN_WIDTH - (text_frame_count.get_width() + 10), text_frame_count.get_height()))
        screen.blit(text_distance, (SCREEN_WIDTH - (text_frame_count.get_width() + 10), text_frame_count.get_height() + text_distance.get_height()))
        pygame.draw.circle(screen, (250, 0, 0), (int(c1[0]), int(c1[1])), 20, 2)
        pygame.draw.circle(screen, (250, 0, 0), (int(c1[0]), int(c1[1])), 2, 2)
        pygame.draw.circle(screen, (0, 250, 0), (int(c2[0]), int(c2[1])), 50, 2)
        pygame.draw.circle(screen, (0, 250, 0), (int(c2[0]), int(c2[1])), 2, 2)
        pygame.display.flip()
        clock.tick(FRAMES_PER_SECOND)

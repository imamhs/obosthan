# Copyright (c) 2019, Md Imam Hossain (emamhd at gmail dot com)
# see LICENSE.txt for details

import pygame
import obosthan


frame_count = 0
FRAMES_PER_SECOND = 25

pygame.init()
screen = pygame.display.set_mode((1024, 768))
pygame.display.set_caption('Obosthan vector example')
pygame.key.set_repeat(1, 10)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)

vec1 = obosthan.OVector2D(100, 100)
vec2 = obosthan.OVector2D(100, 100)
theta = 0
theta1 = 0
x = y = 400

a = obosthan.OPoint2D(x, y)
pp = obosthan.OPolygon([[234, 230], [409, 136], [823, 262], [240, 412]])

done = False
pause = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if pause == False:
                    pause = True
                else:
                    pause = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            a[0] = pygame.mouse.get_pos()[0]
            a[1] = pygame.mouse.get_pos()[1]

        if event.type == pygame.KEYDOWN and pause == False:
            if event.key == pygame.K_w:
                theta = theta - 0.1
                vec2.rotate(theta)
            if event.key == pygame.K_s:
                theta = theta + 0.1
                vec2.rotate(theta)
            if event.key == pygame.K_a:
                theta1 = theta1 - 1
                vec1.rotate(theta1)
            if event.key == pygame.K_d:
                theta1 = theta1 + 1
                vec1.rotate(theta1)

    if pause == False:

        vec3 = vec1.project(vec2)
        print(vec1.angle)

        frame_count = frame_count + 1
        text_frame_count = font.render('Frame count ' + str(frame_count), True, (255, 255, 255))
        text_time = font.render('Time ' + str(frame_count/FRAMES_PER_SECOND), True, (255, 255, 255))
        text_info = font.render('Press A, S, W, D buttons on the keyboard to rotate vectors', True, (255, 200, 200))
        screen.fill((0, 0, 0))
        screen.blit(text_info, (0, text_info.get_height()))
        screen.blit(text_frame_count, (1024 - (text_frame_count.get_width() + 10), text_frame_count.get_height()))
        screen.blit(text_time, (1024 - (text_frame_count.get_width() + 10), text_frame_count.get_height() + text_time.get_height()))
        pygame.draw.circle(screen, (0, 255, 255), (x, y), int(vec1.length), 1)
        pygame.draw.line(screen, (255, 0, 0), (x, y), (x+vec1[0], y+vec1[1]))
        pygame.draw.line(screen, (0, 255, 0), (x, y), (x+vec2[0], y+vec2[1]))
        pygame.draw.line(screen, (0, 0, 255), (x, y), (x+vec3[0], y+vec3[1]), 4)
        pygame.display.flip()
        clock.tick(FRAMES_PER_SECOND)


        #print(round(vec3.angle, 2), round(vec1.angle, 2))

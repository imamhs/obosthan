# Copyright (c) 2019, Md Imam Hossain (emamhd at gmail dot com)
# see LICENSE.txt for details

import pygame
import obosthan

frame_count = 0
FRAMES_PER_SECOND = 25

pygame.init()
screen = pygame.display.set_mode((1024, 768))
pygame.display.set_caption('Obosthan point and vector')
pygame.key.set_repeat(1, 10)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)

vec1 = obosthan.OVector2D(100, 100)
theta = 0
x = y = 300

a = obosthan.OPoint2D(x, y)
b = obosthan.OPoint2D(x, y)

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
                theta = theta - 1
                vec1.rotate(theta)
            if event.key == pygame.K_s:
                theta = theta + 1
                vec1.rotate(theta)

    if pause == False:

        b = a.vector_copy(vec1, 100)

        frame_count = frame_count + 1
        text_frame_count = font.render('Frame count ' + str(frame_count), True, (255, 255, 255))
        text_time = font.render('Time ' + str(frame_count/FRAMES_PER_SECOND), True, (255, 255, 255))
        text_angle = font.render('Vector angle ' + str(round(vec1.angle,3)), True, (255, 255, 255))
        text_info = font.render("Press w and s buttons on the keyboard to rotate vector. Click to change point location.", True, (255, 200, 200))
        screen.fill((0, 0, 0))
        screen.blit(text_info, (0, text_info.get_height()))
        screen.blit(text_frame_count, (1024 - (text_frame_count.get_width() + 50), text_frame_count.get_height()))
        screen.blit(text_time, (1024 - (text_frame_count.get_width() + 50), text_frame_count.get_height() + text_time.get_height()))
        screen.blit(text_angle, (1024 - (text_frame_count.get_width() + 50), text_frame_count.get_height() + text_time.get_height() + text_angle.get_height()))
        pygame.draw.line(screen, (255, 0, 0), (x, y), (x+vec1[0], y+vec1[1]))
        pygame.draw.circle(screen, (0, 55, 255), (int(a[0]), int(a[1])), 5, 5)
        pygame.draw.circle(screen, (55, 55, 255), (int(b[0]), int(b[1])), 5, 5)
        pygame.display.flip()
        clock.tick(FRAMES_PER_SECOND)


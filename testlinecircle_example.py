# Copyright (c) 2019, Md Imam Hossain (emamhd at gmail dot com)
# see LICENSE.txt for details

import pygame
import obosthan

frame_count = 0
FRAMES_PER_SECOND = 25

pygame.init()
screen = pygame.display.set_mode((1024, 768))
pygame.display.set_caption('Obosthan line and circle collision test')
pygame.key.set_repeat(1, 10)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)

vec1 = obosthan.OVector2D(200, 200)
theta = 0
x = y = 300
circle_rgb = [0, 255, 0]

a = obosthan.OPoint2D(x, y)

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

        a[0] = pygame.mouse.get_pos()[0]
        a[1] = pygame.mouse.get_pos()[1]

        if event.type == pygame.KEYDOWN and pause == False:
            if event.key == pygame.K_w:
                theta = theta - 5
                vec1.rotate(theta)
            if event.key == pygame.K_s:
                theta = theta + 5
                vec1.rotate(theta)

    if pause == False:

        l1 = obosthan.OLine2D(300, 300, 300+vec1[0], 300+vec1[1])
        r = obosthan.oline_circle(l1, a, 20)
        d = round(l1.distance_to_point(a), 2)

        if r == None:
            circle_rgb[0] = 0
            circle_rgb[1] = 255
            r = 0
        else:
            circle_rgb[0] = 255
            circle_rgb[1] = 0
            r = round(r, 2)

        frame_count = frame_count + 1
        text_frame_count = font.render('Frame count ' + str(frame_count), True, (255, 255, 255))
        text_time = font.render('Time ' + str(frame_count/FRAMES_PER_SECOND), True, (255, 255, 255))
        text_distance = font.render('Distance ' + str(d), True, (255, 255, 255))
        text_penetration = font.render('Penetration ' + str(r), True, (255, 255, 255))
        screen.fill((0, 0, 0))
        screen.blit(text_frame_count, (1024 - (text_frame_count.get_width() + 20), text_frame_count.get_height()))
        screen.blit(text_time, (1024 - (text_frame_count.get_width() + 20), text_frame_count.get_height() + text_time.get_height()))
        screen.blit(text_distance, (1024 - (text_frame_count.get_width() + 20), text_frame_count.get_height() + text_time.get_height() + text_distance.get_height()))
        screen.blit(text_penetration, (1024 - (text_frame_count.get_width() + 20), text_frame_count.get_height() + text_time.get_height() + text_distance.get_height()+ text_penetration.get_height()))
        pygame.draw.line(screen, (255, 0, 0), (l1[0], l1[1]), (l1[2], l1[3]))
        pygame.draw.circle(screen, (circle_rgb[0], circle_rgb[1], circle_rgb[2]), (int(a[0]), int(a[1])), 20, 2)
        pygame.display.flip()
        clock.tick(FRAMES_PER_SECOND)

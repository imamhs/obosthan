# Copyright (c) 2019, Md Imam Hossain (emamhd at gmail dot com)
# see LICENSE.txt for details

import pygame
import obosthan

frame_count = 0
FRAMES_PER_SECOND = 25

pygame.init()
screen = pygame.display.set_mode((1024, 768))
pygame.display.set_caption('Obosthan polygon and transformation')
pygame.key.set_repeat(1, 10)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)

pp = obosthan.OPolygon(((329, 154), (661, 181), (545, 280)))

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

        if event.type == pygame.KEYDOWN and pause == False:
            if event.key == pygame.K_q:
                pp.rotate_centroid(5)
                pp.translate(0.2,0.2)
            if event.key == pygame.K_a:
                pp.scale_point(1.1, 1.1, pp.get_point(0))
            if event.key == pygame.K_d:
                pp.scale_point(0.9, 0.9, pp.get_point(0))

    if pause == False:

        aabb = pp.get_AABB()

        frame_count = frame_count + 1
        text_frame_count = font.render('Frame count ' + str(frame_count), True, (255, 255, 255))
        text_time = font.render('Time ' + str(frame_count/FRAMES_PER_SECOND), True, (255, 255, 255))
        text_info = font.render('Press Q button on the keyboard' , True, (255, 200, 200))
        screen.fill((0, 0, 0))
        pygame.draw.polygon(screen, (0, 50, 100), aabb.coords)
        pygame.draw.polygon(screen, (255, 0, 0), pp.coords)
        pygame.draw.circle(screen, (10, 10, 10), (int(pp.centroid[0]), int(pp.centroid[1])), 5, 5)
        screen.blit(text_info, (0, text_info.get_height()))
        screen.blit(text_frame_count, (1024 - (text_frame_count.get_width() + 10), text_frame_count.get_height()))
        screen.blit(text_time, (1024 - (text_frame_count.get_width() + 10), text_frame_count.get_height() + text_time.get_height()))
        pygame.display.flip()
        clock.tick(FRAMES_PER_SECOND)

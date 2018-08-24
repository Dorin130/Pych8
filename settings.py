import numpy as np
import pygame

SCALE = 20
STEP_PERIOD = 1 / 540
CLOCK_PERIOD = 1 / 60
KEYS = {pygame.K_6: 0x1, pygame.K_7: 0x2, pygame.K_8:0x3, pygame.K_9: 0xc,
        pygame.K_y: 0x4, pygame.K_u: 0x5, pygame.K_i:0x6, pygame.K_o: 0xd,
        pygame.K_h: 0x7, pygame.K_j: 0x8, pygame.K_k:0x9, pygame.K_l: 0xe,
        pygame.K_n: 0xa, pygame.K_m: 0x0, pygame.K_COMMA:0xb, pygame.K_PERIOD: 0xf
        }


SAMPLERATE = 44100
sound_wave = np.array([4096 * np.sin(2.0 * np.pi * 440 * x / SAMPLERATE) for x in range(0, SAMPLERATE)]).astype(np.int16)


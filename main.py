import time
import argparse
from settings import *
from ch8 import Ch8State


def main():
    pygame.mixer.pre_init(SAMPLERATE, -16, 1)
    pygame.init()

    parser = argparse.ArgumentParser()
    parser.add_argument("rom", help="rom file")
    args = parser.parse_args()

    rom = args.rom
    ch8 = Ch8State()
    ch8.load_ram(rom)

    pygame.display.set_caption('Pych8')
    screen = pygame.display.set_mode((64 * SCALE, 32 * SCALE))

    t_step = time.monotonic()
    t_clock = time.monotonic()

    while True:
        if pygame.event.get(pygame.QUIT): break

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                ch8 = Ch8State()
                ch8.load_ram(rom)
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if event.key in KEYS.keys():
                    ch8.process_key(event.type, event.key)

        if time.monotonic() - t_step >= STEP_PERIOD:
            ch8.step()
            t_step = time.monotonic()
        if time.monotonic() - t_clock >= CLOCK_PERIOD:
            ch8.clock()
            t_clock = time.monotonic()

        if ch8.display.change:
            ch8.display.change = False
            arr = np.full((32, 64), 255, dtype="int")
            mask = ch8.display.get_display()
            arr[~mask] = 0

            surface = pygame.transform.scale(pygame.surfarray.make_surface(arr.T), (64 * SCALE, 32 * SCALE))
            screen.blit(surface, (0, 0))
            pygame.display.flip()


if __name__ == "__main__":
    main()
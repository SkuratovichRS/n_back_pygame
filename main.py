import asyncio

import pygame

from app.factory import Factory

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    factory = Factory()
    asyncio.run(factory.run())

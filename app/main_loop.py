import asyncio

import pygame

from app.constants import States
from app.game import GameWindow
from app.menu import MenuWindow, RulesWindow, DifficultyWindow


async def main_loop(menu_window: MenuWindow, rules_window: RulesWindow, difficulty_window: DifficultyWindow,
                    game_window: GameWindow) -> None:
    states = {
        States.MENU: menu_window,
        States.RULES: rules_window,
        States.DIFFICULTY: difficulty_window,
        States.GAME: game_window,
    }
    current_state = States.MENU
    prev_state = current_state
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
        if not running:
            break
        state_object = states.get(current_state)
        if state_object is game_window and prev_state == States.DIFFICULTY:
            state_object.difficulty = states.get(prev_state).difficulty
            state_object.start_time = pygame.time.get_ticks()

        prev_state = current_state
        state_object.draw()

        if state_object.next_state != current_state:
            current_state = state_object.next_state
            state_object.next_state = prev_state

        await asyncio.sleep(0)
        clock.tick(60)

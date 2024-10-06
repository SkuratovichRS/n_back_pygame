import random

import pygame

from app.base_window import BaseWindow
from app.constants import Colors, States, LETTERS, SOUNDS_PATH


class GameWindow(BaseWindow):
    def __init__(self):
        self.next_state = States.GAME
        self.start_time = None
        self.difficulty = None
        self._width = 600
        self._height = 600
        self._background_color = Colors.GRAY
        self._window = None
        self._attempt = 1
        self._interval = 2000
        self._chance = (True, True, False, False, False)
        self._rect_position = self._get_rect_position()
        self._current_letter = self._get_letter()
        self._positions_storage = {self._attempt: (self._rect_position, self._current_letter)}
        self._goal = 0
        self._correct = 0
        self._rect_in_position = False
        self._letter_in_position = False
        self._play_sound = True

    def draw(self) -> None:
        if self._window is None or self._window.get_size() != (self._width, self._height):
            self._window = pygame.display.set_mode((self._width, self._height))
        if self.finish_game():
            self._result_screen()
        else:
            self._window.fill(self._background_color)
            self._field()
            self._back_button()
            self._attempts_displaying()
            if self._change_position():
                self._play_sound = True
                n_back_position = self._attempt - self.difficulty
                if self._positions_storage.get(n_back_position):
                    n_back_rect_position, n_back_letter_position = self._positions_storage.get(n_back_position)[0], \
                        self._positions_storage.get(n_back_position)[1]
                else:
                    n_back_rect_position, n_back_letter_position = None, None
                same_rect = random.choice(self._chance)
                same_letter = random.choice(self._chance)
                if same_rect and n_back_rect_position:
                    self._rect_position = n_back_rect_position
                    self._rect_in_position = True
                else:
                    self._rect_position = self._get_rect_position()
                    self._rect_in_position = False
                if same_letter and n_back_letter_position:
                    self._current_letter = n_back_letter_position
                    self._letter_in_position = True
                else:
                    self._current_letter = self._get_letter()
                    self._letter_in_position = False
                if self._rect_position == n_back_rect_position:
                    self._goal += 1
                if self._current_letter == n_back_letter_position:
                    self._goal += 1
                self._attempt += 1
                self._save_position(self._rect_position, self._current_letter)
            self._draw_rect(self._rect_position)
            if self._play_sound and self.next_state == States.GAME:
                self._sound_letter(self._current_letter)
                self._play_sound = False
            if self._rect_button() and self._rect_in_position:
                self._correct += 1
                self._rect_in_position = False
            if self._sound_button() and self._letter_in_position:
                self._correct += 1
                self._letter_in_position = False
            pygame.display.flip()

    def _field(self) -> None:
        color = Colors.WHITE
        field_width = 390
        field_height = 390
        line_width = 1
        width_diff = (self._width - field_width) // 2
        height_diff = (self._height - field_height) // 2

        pygame.draw.line(self._window, color, (width_diff, height_diff),
                         (width_diff, field_height + height_diff), line_width)
        pygame.draw.line(self._window, color, (width_diff + field_width // 3, height_diff),
                         (width_diff + field_width // 3, field_height + height_diff), line_width)
        pygame.draw.line(self._window, color, (width_diff + field_width * 2 // 3, height_diff),
                         (width_diff + field_width * 2 // 3, field_height + height_diff), line_width)
        pygame.draw.line(self._window, color, (width_diff + field_width, height_diff),
                         (width_diff + field_width, field_height + height_diff), line_width)

        pygame.draw.line(self._window, color, (width_diff, height_diff),
                         (width_diff + field_width, height_diff), line_width)
        pygame.draw.line(self._window, color, (width_diff, height_diff + field_height // 3),
                         (width_diff + field_width, height_diff + field_height // 3), line_width)
        pygame.draw.line(self._window, color, (width_diff, height_diff + field_height * 2 // 3),
                         (width_diff + field_width, height_diff + field_height * 2 // 3), line_width)
        pygame.draw.line(self._window, color, (width_diff, height_diff + field_height),
                         (width_diff + field_width, height_diff + field_height), line_width)

    def _draw_rect(self, position: tuple[int]) -> None:
        rect_width = 100
        rect_height = 100
        rect = pygame.Rect(position[0], position[1], rect_width, rect_height)
        pygame.draw.rect(self._window, Colors.SKY_BLUE, rect)

    @staticmethod
    def _get_rect_position() -> tuple:
        positions = [
            (120, 120), (250, 120), (380, 120),
            (120, 250), (250, 250), (380, 250),
            (120, 380), (250, 380), (380, 380),
        ]
        return random.choice(positions)

    @staticmethod
    def _get_letter() -> str:
        return random.choice(LETTERS)

    @staticmethod
    def _sound_letter(letter: str) -> None:
        sound = pygame.mixer.Sound(f"{SOUNDS_PATH}/{letter}.mp3")
        sound.play()

    def _back_button(self) -> None:
        font = pygame.font.Font(None, 36)
        rect_width = 180
        rect_height = 50
        rect = pygame.Rect(10, 10, rect_width, rect_height)
        button_color = Colors.DARK_GREEN if rect.collidepoint(pygame.mouse.get_pos()) else Colors.GREEN
        pygame.draw.rect(self._window, button_color, rect)
        text = font.render('Back to menu', True, Colors.BLACK)
        text_rect = text.get_rect(center=rect.center)
        self._window.blit(text, text_rect)
        if rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.next_state = States.MENU
            self._restart_game()

    def _attempts_displaying(self) -> None:
        font = pygame.font.Font(None, 36)
        text = font.render(f'Attempt: {self._attempt}', True, Colors.WHITE)
        text_width, text_height = text.get_size()
        self._window.blit(text, (self._width - text_width - 10, 10))

    def _save_position(self, rect_position: tuple, letter: str) -> None:
        self._positions_storage[self._attempt] = (rect_position, letter)

    def _change_position(self) -> bool:
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time <= self._interval:
            return False
        self.start_time = current_time
        return True

    def _rect_button(self) -> bool:
        font = pygame.font.Font(None, 36)
        rect_width = 180
        rect_height = 50
        rect = pygame.Rect(105, 510, rect_width, rect_height)
        button_color = Colors.DARK_GREEN if rect.collidepoint(pygame.mouse.get_pos()) else Colors.GREEN
        pygame.draw.rect(self._window, button_color, rect)
        text = font.render('Position', True, Colors.WHITE)
        text_rect = text.get_rect(center=rect.center)
        self._window.blit(text, text_rect)
        if rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return True
        return False

    def _sound_button(self) -> bool:
        font = pygame.font.Font(None, 36)
        rect_width = 180
        rect_height = 50
        rect = pygame.Rect(self._width - 105 - rect_width, 510, rect_width, rect_height)
        button_color = Colors.DARK_GREEN if rect.collidepoint(pygame.mouse.get_pos()) else Colors.GREEN
        pygame.draw.rect(self._window, button_color, rect)
        text = font.render('Sound', True, Colors.WHITE)
        text_rect = text.get_rect(center=rect.center)
        self._window.blit(text, text_rect)
        if rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return True
        return False

    def _score_displaying(self):
        font = pygame.font.Font(None, 72)
        score = round((self._correct / self._goal * 100), 2) if self._goal != 0 else 100
        text = font.render(f'Your score: {score}%', True, Colors.WHITE)
        text_width, text_height = text.get_size()
        self._window.blit(text, ((self._width - text_width) // 2, (self._height - text_height) // 2))

    def _restart_game(self) -> None:
        self._attempt = 1
        self._rect_position = self._get_rect_position()
        self._current_letter = self._get_letter()
        self._positions_storage = {self._attempt: (self._rect_position, self._current_letter)}
        self._goal = 0
        self._correct = 0
        self._rect_in_position = False
        self._letter_in_position = False
        self._play_sound = True

    def _result_screen(self) -> None:
        self._window.fill(self._background_color)
        self._back_button()
        self._score_displaying()
        pygame.display.flip()

    def finish_game(self) -> bool:
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time <= self._interval:
            return False
        if self._attempt >= 20:
            return True

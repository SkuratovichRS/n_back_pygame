import pygame

from app.base_window import BaseWindow
from app.constants import Colors, States


class MenuWindow(BaseWindow):
    def __init__(self):
        self.next_state = States.MENU
        self._width = 600
        self._height = 600
        self._background_color = Colors.GRAY
        self._window = None

    def draw(self) -> None:
        if self._window is None or self._window.get_size() != (self._width, self._height):
            self._window = pygame.display.set_mode((self._width, self._height))
        pygame.display.set_caption('N-back')
        self._window.fill(self._background_color)
        self._start_game_button()
        self._rules_button()
        pygame.display.flip()

    def _start_game_button(self) -> None:
        font = pygame.font.Font(None, 72)
        rect_width = 300
        rect_height = 72
        rect = pygame.Rect((self._width - rect_width) // 2, self._height // 2 - 150, rect_width, rect_height)
        button_color = Colors.DARK_GREEN if rect.collidepoint(pygame.mouse.get_pos()) else Colors.GREEN
        pygame.draw.rect(self._window, button_color, rect)
        text = font.render('Start game', True, Colors.WHITE)
        text_rect = text.get_rect(center=rect.center)
        self._window.blit(text, text_rect)
        if rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.next_state = States.DIFFICULTY

    def _rules_button(self) -> None:
        font = pygame.font.Font(None, 72)
        rect_width = 180
        rect_height = 72
        rect = pygame.Rect((self._width - rect_width) // 2, self._height // 2 + 50, rect_width, rect_height)
        button_color = Colors.DARK_GREEN if rect.collidepoint(pygame.mouse.get_pos()) else Colors.GREEN
        pygame.draw.rect(self._window, button_color, rect)
        text = font.render('Rules', True, Colors.BLACK)
        text_rect = text.get_rect(center=rect.center)
        self._window.blit(text, text_rect)
        if rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.next_state = States.RULES


class RulesWindow(BaseWindow):
    def __init__(self):
        self.next_state = States.RULES
        self._width = 600
        self._height = 600
        self._background_color = Colors.GRAY
        self._window = None

    def draw(self) -> None:
        if self._window is None or self._window.get_size() != (self._width, self._height):
            self._window = pygame.display.set_mode((self._width, self._height))
        self._window.fill(self._background_color)
        self._rules_text()
        self._back_button()
        pygame.display.flip()

    def _rules_text(self) -> None:
        font = pygame.font.Font(None, 36)
        text = (
            'Dual N-Back is a memory game where you track both a square’s position on a grid and a spoken letter, '
            'pressing buttons when either the current position or letter matches the ones from "N" turns back.')
        words = text.split(' ')
        lines = []
        current_line = ''
        text_width, text_height = 0, 0

        for word in words:
            test_line = current_line + word + ' '
            text_width, text_height = font.size(test_line)
            if text_width > self._width:
                lines.append(current_line)
                current_line = word + ' '
            else:
                current_line = test_line

        lines.append(current_line)
        total_height = len(lines) * text_height
        y = (self._height - total_height) // 2

        for line in lines:
            text = font.render(line, True, Colors.WHITE)
            line_width, line_height = text.get_size()
            x = (self._width - line_width) // 2
            self._window.blit(text, (x, y))
            y += line_height

    def _back_button(self) -> None:
        font = pygame.font.Font(None, 36)
        rect_width = 180
        rect_height = 72
        rect = pygame.Rect(10, self._height - rect_height - 10, rect_width, rect_height)
        button_color = Colors.DARK_GREEN if rect.collidepoint(pygame.mouse.get_pos()) else Colors.GREEN
        pygame.draw.rect(self._window, button_color, rect)
        text = font.render('Back', True, Colors.BLACK)
        text_rect = text.get_rect(center=rect.center)
        self._window.blit(text, text_rect)
        if rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.next_state = States.MENU


class DifficultyWindow(BaseWindow):
    def __init__(self):
        self.next_state = States.DIFFICULTY
        self.difficulty = None
        self._width = 600
        self._height = 600
        self._background_color = Colors.GRAY
        self._window = None

    def draw(self) -> None:
        if self._window is None or self._window.get_size() != (self._width, self._height):
            self._window = pygame.display.set_mode((self._width, self._height))
        self._window.fill(self._background_color)
        self._title_text()
        self._difficulty_button(1, 50)
        self._difficulty_button(2, 162.5)
        self._difficulty_button(3, 275)
        self._difficulty_button(4, 387.5)
        self._difficulty_button(5, 500)
        self._back_button()
        pygame.display.flip()

    def _title_text(self) -> None:
        font = pygame.font.Font(None, 54)
        title_text = 'Choose "N"'
        text_width, text_height = font.size(title_text)
        rendered_title_text = font.render(title_text, True, Colors.WHITE)
        self._window.blit(rendered_title_text,
                          ((self._width - text_width) // 2, (self._height - text_height) // 2 - 100))

    def _difficulty_button(self, number: int, position: float) -> None:
        font = pygame.font.Font(None, 54)
        rect_width = 50
        rect_height = 50
        rect = pygame.Rect((position, (self._height - rect_height) // 2, rect_width, rect_height))
        button_color = Colors.DARK_GREEN if rect.collidepoint(pygame.mouse.get_pos()) else Colors.GREEN
        pygame.draw.rect(self._window, button_color, rect)
        text = font.render(str(number), True, Colors.WHITE)
        text_rect = text.get_rect(center=rect.center)
        self._window.blit(text, text_rect)
        if rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.difficulty = number
            self.next_state = States.GAME

    def _back_button(self) -> None:  # avoiding duplication leads to unnecessary complications
        font = pygame.font.Font(None, 36)
        rect_width = 180
        rect_height = 72
        rect = pygame.Rect(10, self._height - rect_height - 10, rect_width, rect_height)
        button_color = Colors.DARK_GREEN if rect.collidepoint(pygame.mouse.get_pos()) else Colors.GREEN
        pygame.draw.rect(self._window, button_color, rect)
        text = font.render('Back', True, Colors.BLACK)
        text_rect = text.get_rect(center=rect.center)
        self._window.blit(text, text_rect)
        if rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.next_state = States.MENU

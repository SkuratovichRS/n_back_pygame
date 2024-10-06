from app.game import GameWindow
from app.main_loop import main_loop
from app.menu import MenuWindow, RulesWindow, DifficultyWindow


class Factory:

    async def run(self) -> None:
        menu_window = self._create_menu_window()
        rules_window = self._create_rules_window()
        difficulty_window = self._create_difficulty_window()
        game_window = self._create_game_window()
        await main_loop(menu_window, rules_window, difficulty_window, game_window)

    @staticmethod
    def _create_menu_window() -> MenuWindow:
        return MenuWindow()

    @staticmethod
    def _create_rules_window() -> RulesWindow:
        return RulesWindow()

    @staticmethod
    def _create_difficulty_window() -> DifficultyWindow:
        return DifficultyWindow()

    @staticmethod
    def _create_game_window() -> GameWindow:
        return GameWindow()

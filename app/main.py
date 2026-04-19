from textual.app import App

from app.screens.game_screen import GameScreen


class DeepSeaHorrorApp(App):
    CSS_PATH = "app.tcss"
    TITLE = "Deep Sea Horror"
    SUB_TITLE = "Mock Gameplay UI"

    def on_mount(self) -> None:
        self.push_screen(GameScreen())


if __name__ == "__main__":
    DeepSeaHorrorApp().run()
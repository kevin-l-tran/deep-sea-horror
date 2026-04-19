from textual.app import App

from app.screens.game_screen import GameScreen

from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    filename="deep_sea_horror.log",
    format="%(asctime)s %(levelname)s %(name)s:%(lineno)d - %(message)s",
    force=True,
)

class DeepSeaHorrorApp(App):
    CSS_PATH = "app.tcss"
    TITLE = "Deep Sea Horror"
    SUB_TITLE = "Mock Gameplay UI"

    def on_mount(self) -> None:
        self.push_screen(GameScreen())

if __name__ == "__main__":
    DeepSeaHorrorApp().run()

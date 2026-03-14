from game.level_manager import BaseLevel


class Level1(BaseLevel):
    level_number = 1
    title = "Normal Space"

    def __init__(self):
        super().__init__()
        self.status_message = "Tutorial: place 8 planets in orbit"

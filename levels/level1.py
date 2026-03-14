from game.level_manager import BaseLevel


class Level1(BaseLevel):
    level_number = 1
    title = "Normal Space"

    def __init__(self):
        super().__init__()
        self.required_planets = 5
        self.status_message = "Tutorial: Place 5 planets in orbit. Learn about the solar system!"

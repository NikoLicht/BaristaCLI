from .game_object import GameObject
from components import *
from src.printing import *
from src.state import Physical, Temperature

class Water(GameObject):
    def __init__(self, game_instance):
        super().__init__(game_instance)
        self.name = "water"
        self.AddComponent(Drinkable())
        self.AddComponent(Watchable("It has a weirdness to it."))
        self.AddComponent(Container())
        self.AddComponent(Slapable(f"{thing("Water")} splashes everywhere! It is quite humorous!"))
        self.property = Physical.LIQUID
        self.add_taste("calcium", 0.1, 0.1)
        self.add_taste("wet", 0.1, 0.1)
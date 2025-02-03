from .game_object import GameObject
from components import *
from src.printing import *
from src.state import Physical, Verbs

class Water(GameObject):
    def __init__(self, game_instance):
        super().__init__(game_instance)
        self.name = "water"
        self.AddComponent(Drinkable("watery"))
        self.AddComponent(Watchable("It has a weirdness to it."))
        self.AddComponent(Container())
        self.AddComponent(Slapable(f"{thing("Water")} splashes everywhere! It is quite humorous!"))
        self.flavour_impact = ["mild"]
        self.property = Physical.LIQUID

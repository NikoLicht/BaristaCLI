from .game_object import GameObject
from components import *
from state import Physical

class Beans(GameObject):
    def __init__(self, game_instance):
        super().__init__(game_instance)
        self.name = "beans"
        self.AddComponent(Edible("bitter"))
        self.AddComponent(Watchable("Tiny little brown things with an almost burned exterior."))
        self.AddComponent(Slapable("Maybe to impact flavour?"))
        self.flavour_impact = ["bitter"]
        self.property = Physical.SOLID
        self.spelling = {
            "it" : "they",
            "is" : "are"
        }
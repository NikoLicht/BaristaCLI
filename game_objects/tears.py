from components import *
from game_objects import *
from src.printing import *
from src.state import Physical
from src.grammar import Grammar

class Tears(GameObject):
    def __init__(self, game_instance):
        super().__init__(game_instance)
        self.name = "tears"
        self.property = Physical.LIQUID
        self.flavour_impact = ["salt"]
        self.AddComponent(Watchable(f"You feel proud, because you made it. It looks like an ordinary {thing(self.name)}"))
        self.AddComponent(Drinkable())
        self.AddComponent(Slapable(f"The {thing(self.name)} cannot hurt you anymore."))
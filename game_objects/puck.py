from game_objects.game_object import GameObject
from components import Watchable, Edible
from src.state import Physical
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.coffee_factory import ExtractionResult

class Puck(GameObject):
    def __init__(self, game_instance, *args):
        super().__init__(game_instance, *args)
        self.property = Physical.SOLID
        self.add_taste("muddy", 0.6, 5)
        self.in_mixture = []
        self.name = "Puck"
        self.lore = "This is the remains left over after having extracted (almost) all the liquid."
        self.AddComponent(Watchable("Upon close inspection, you realize, that perhaps you press too hard, or maybe your grinds are too coarse."))
        self.AddComponent(Edible("It is simply too tempting. You take a big bite of the brownie-like result. Instantly your face reads regret."))

    def setup(self, extract: "ExtractionResult"):
        if extract:
            if extract.flavors:
                for flavour in extract.flavors:
                    self.add_taste(flavour, 1.0, extract.flavors[flavour])

        
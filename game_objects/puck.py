from game_objects import *
from components import *
from src.state import Physical
from typing import List

class Puck(GameObject):
    def __init__(self, game_instance, *args):
        super().__init__(game_instance, *args)
        self.property = Physical.SOLID
        self.flavour_impact = ["muddy"]
        self.in_mixture = []
        self.name = "Puck"
        self.AddComponent(Watchable("Upon close inspection, you realize, that perhaps you press too hard, or maybe your grinds are too coarse."))
        self.AddComponent(Edible("It is simply too tempting. You take a big bite of the brownie-like result. Instantly your face reads regret."))

    def setup(self, content: List[GameObject]):
        for obj in content:
            self.flavour_impact.extend(obj.flavour_impact)
            if isinstance(obj, Mixture):
                self.in_mixture.extend(obj.in_mixture)
            else:
                self.in_mixture.append(obj)


        
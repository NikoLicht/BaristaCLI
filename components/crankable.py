from src.printing import *
from .component import Component

class Crankable(Component):
    def __init__(self, crank_linked_func):
        super().__init__()
        self.add_method(["crank"], self.crank)
        self.crank_linked_func = crank_linked_func

    def crank(self):
        say(f"You {action("crank")} the handle on the {thing(self.owner.name)}. The action is completely smooth, because of the superb ball-bearings.")
        self.crank_linked_func()

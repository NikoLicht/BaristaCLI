from .component import Component
from printing import *

class Drinkable(Component):
    def __init__(self, taste):
        super().__init__()
        self.add_method(["drink"], self.drink)
        self.taste = taste

    def drink(self):
        if self.owner.has_state("hot"):
            say(f"You burn yourself on the boiling hot {thing(self.owner.name)}")
        else:
            say(f"You {action("drink")} the {thing(self.owner.name)}, quite refreshing. It tastes a bit {self.taste}.")
        self.owner.add_state("consumed")
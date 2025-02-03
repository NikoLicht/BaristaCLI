from .component import Component
from printing import *

class Powered(Component):
    def __init__(self, when_turn_on = None):
        super().__init__()
        self.add_method(["turn-on"], self.turn_on)
        self.when_turn_on: function = when_turn_on

    def turn_on(self):
        say(f"You {action("turn-on")} the {thing(self.owner.name)}, a little funny sound emerges, as usual.")
        self.owner.add_state("turned_on")
        if self.when_turn_on is not None:
            self.when_turn_on()
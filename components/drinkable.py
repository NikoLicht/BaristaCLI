from .component import Component
from src.printing import *
from src.grammar import Grammar
from src.action_object import ActionObject

class Drinkable(Component):
    def __init__(self, flavour_text = None):
        super().__init__()
        self.add_method(ActionObject("drink", None, methods=[self.drink]))
        self.flavour_text = flavour_text

    def drink(self):
        gr = Grammar()
        if self.owner.has_state("hot"):
            say(f"You burn yourself on the boiling hot {thing(self.owner.name)}")
        else:
            if self.flavour_text is not None:
                say(f"You {action("drink")} the {thing(self.owner.name)}. {self.flavour_text}")
            else:
                say(f"You {action("drink")} the {thing(self.owner.name)}, quite refreshing. While swirling it around in your mouth, you detect notes of {gr.make_list(self.owner.flavour_impact)}")
        self.owner.add_state("consumed")
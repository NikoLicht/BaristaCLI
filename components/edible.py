from components import *
from printing import *
from grammar import Grammar

class Edible(Component):
    def __init__(self, taste):
        super().__init__()
        self.add_method(["eat"], self.eat)
        self.taste = taste

    def eat(self, triggered_action = False):
        gr = Grammar()
        if self.owner.has_state("hot"):
            say(f"You burn yourself on the boiling hot {thing(self.owner.name)}. You can't taste anything right now.")
        else:
            say(f"You {action("eat")} the {thing(self.owner.name)}. It has quite a {gr.make_list(self.owner.flavour_impact)} aftertaste.")
        self.owner.add_state("consumed")

        container: Container = self.owner.get_component("container")
        if container:
            container.recursive_action("eat", True)

    
from components import *
from printing import *
import random
from grammar import Grammar
from state import Physical

class Slapable(Component):
    def __init__(self, flavour_text):
        super().__init__()
        self.add_method(["slap"], self.slap)
        self.slap_sounds = ["Whack!", "SLAP!", "Smack!"]
        self.flavour_text = flavour_text
    
    def slap(self):

        if self.owner.position is not None:
            say(f"You cannot {action("slap")} something that is inside another thing.")
            return

        grammar = Grammar()
        say(f"{random.choice(self.slap_sounds)} You give the {thing(self.owner.name)} a proper {action("slap")}, for some reason. {self.flavour_text}")

        container: Container = self.owner.get_component("container")
        if container:
            if len(container.contains) > 0:
                say(f"As a consequence, the {grammar.make_list(container.contains)} spill out of the {thing(self.owner.name)}.")
                for obj in container.contains:
                    obj.position = None
                container.contains = []
                
                    



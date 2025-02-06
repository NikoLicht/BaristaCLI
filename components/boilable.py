from .component import Component
from .container import Container
from src.printing import *
from src.action_object import ActionObject

class Boilable(Component):
    """A component that makes an object boilable."""
    def __init__(self):
        super().__init__()
        self.add_method(ActionObject("boil", None, methods=[self.boil]))

    def boil(self, triggered_action = False):
        if not triggered_action:
            say(f"You boil the {thing(self.owner.name)}.")
        else:
            say(f"You also boil the {thing(self.owner.name)} because {self.owner.position.name} contains the {thing(self.owner.name)}")
        self.owner.add_state("hot")

        container : Container = self.owner.get_component("container")
        if container is not None:
            container.recursive_action("boil", True)
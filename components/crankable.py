from src.printing import *
from .component import Component
from src.state import Physical
from src.action_object import ActionObject

class Crankable(Component):
    def __init__(self, crank_linked_func):
        super().__init__()
        self.add_method(ActionObject("crank", None, methods=[self.crank]))
        self.crank_linked_func = crank_linked_func

    def crank(self):
        if self.owner.property is not Physical.SOLID:
            say(f"Hmm. The {thing(self.owner.name)} seems a little bit [italic]{self.owner.property.name.lower()}y now[/ italic], you have a hard time cranking anything.")
            return
        say(f"You {action("crank")} the handle on the {thing(self.owner.name)}. The action is completely smooth, because of the superb ball-bearings.")
        self.crank_linked_func()

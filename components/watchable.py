from .component import Component
from src.printing import *

class Watchable(Component):
    def __init__(self, flavour_text, on_watch: callable = None):
        super().__init__()
        self.add_method(["watch"], self.watch)
        self.flavour_text = flavour_text
        self.on_watch = on_watch

    def watch(self):
        if self.owner.position is not None:
            say(f"It is quite hard to see the {thing(self.owner.name)}, as it is inside of the {self.owner.position.name}")
        else:
            say(f"You watch the {thing(self.owner.name)} closely. {self.flavour_text}")
        
        if self.on_watch is not None:
            self.on_watch()
from game_objects import *
from components import *
from src.printing import *
from src.grammar import Grammar
from src.state import Physical, Temperature

class Kettle(GameObject):
    def __init__(self, game):
        super().__init__(game)
        self.name = "kettle"
        self.lore = "It is a goosneck kettle."
        self.AddComponent(Powered(self.boil_contents))
        self.AddComponent(Watchable(f"It does seem to be a {thing(self.name)}. Very interesting."))
        self.AddComponent(Slapable(f"With your dead-fish-like hands, you manage to knock over the {thing(self.name)}."))
        self.container: Container = self.AddComponent(Container())
        self.add_taste("calcium", 0.5, 3)
        self.property = Physical.SOLID

    def boil_contents(self):
        grammar = Grammar()
        kettle_content = self.container.get_contents([])
        for content in kettle_content:
            content.add_state(Temperature.HOT)
        say(f"The {grammar.make_list(kettle_content)} is now boiling hot")


from components import *
from game_objects import *
from src.printing import *
from src.state import Physical
from src.grammar import Grammar
from src.action_object import ActionObject

class Tea(GameObject):
    def __init__(self, game_instance):
        super().__init__(game_instance)
        self.flavour_impact = ["cardboard", "regret-like"]
        self.property = Physical.SAND
        self.name = "tea"
        self.game_instance = game_instance
        self.AddComponent(Edible(f"The {thing("tea")} suck all the moisture from your mouth, in exchange for the taste of bitter dried leafes."))
        self.AddComponent(Watchable("It appears as a mix between leafy and pointless. Interesting."))
        self.register_callable_method(ActionObject("dispose", None), self.dispose)

    def dispose(self):
        say(f"You joyfully {action("dispose")} of the {thing(self.name)}. You are right. Let's get rid of this terrible pile of dried leaves.")
        self.game_instance.destroy_game_object([self])
        

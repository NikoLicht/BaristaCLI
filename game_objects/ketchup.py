from game_objects import *
from components import *
from src.state import Physical
from src.printing import *

class Ketchup(GameObject):
    def __init__(self, game_instance):
        super().__init__(game_instance)
        self.name = "ketchup"
        self.lore = f"Hmm, it has been in the {thing("fridge")} for quite some time. It is a Heinz bottle."
        self.AddComponent(Drinkable())
        self.AddComponent(Watchable("The color is somehwat disturbing."))
        self.AddComponent(Container())
        self.AddComponent(Edible("Its a rather acidic and thick sensation."))
        self.AddComponent(Slapable(f"Everything is now semi-covered in {thing("ketchup")}. What a mess."))
        self.flavour_impact = ["vinegar", "tomato-like"]
        self.property = Physical.LIQUID
    
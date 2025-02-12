from .game_object import GameObject
from components import *
from src.state import Physical
from random import choice

class Beans(GameObject):
    def __init__(self, game_instance):
        super().__init__(game_instance)
        self.name = "beans"
        self.flavour_impact = []
        self.origin_country = None
        self.coffee_flavour = None
        self.roast = None
        self.set_origin()
        self.lore = f"These beans are ethically sourced from {self.origin_country}. It seems to be a {self.roast} roast. They are single origin."
        self.weight = 18
        self.AddComponent(Edible())
        self.AddComponent(Watchable("Tiny little brown things with an almost burned exterior."))
        self.AddComponent(Slapable("Maybe to impact flavour?"))
        self.AddComponent(Throwable())
        self.property = Physical.SOLID
        self.spelling = {
            "it" : "they",
            "is" : "are"
        }

    def set_origin(self):
        coffee_flavors = {
            "Brazil": {"flavour": ["nutty", "chocolatey", "low acidity"]},
            "Colombia": {"flavour": ["caramel", "fruity", "well-balanced"]},
            "Ethiopia": {"flavour": ["floral", "citrus", "wine-like"]},
            "Kenya": {"flavour": ["berry-like", "bright acidity", "full-bodied"]},
            "Guatemala": {"flavour": ["chocolatey", "spicy", "full-bodied"]},
            "Costa Rica": {"flavour": ["citrusy", "clean", "balanced"]},
            "Honduras": {"flavour": ["sweet", "nutty", "mild acidity"]},
            "Mexico": {"flavour": ["chocolatey", "light-bodied", "nutty"]},
            "Vietnam": {"flavour": ["bold", "earthy", "bitter"]},
            "Indonesia": {"flavour": ["earthy", "spicy", "full-bodied"]},
            "Peru": {"flavour": ["mild", "nutty", "chocolatey"]},
            "India": {"flavour": ["spicy", "full-bodied", "low acidity"]},
            "Tanzania": {"flavour": ["berry-like", "bright", "winey"]},
            "Rwanda": {"flavour": ["floral", "fruity", "tea-like"]},
            "Yemen": {"flavour": ["spicy", "winey", "complex"]},
        }
        self.origin_country = choice(list(coffee_flavors))
        self.coffee_flavour = coffee_flavors[self.origin_country]["flavour"]
        self.flavour_impact.append(choice(self.coffee_flavour))
        self.flavour_impact.append(choice(self.coffee_flavour))
        self.roast = choice(["light", "medium", "dark"])
        append_to_flavour = ""
        match(self.roast):
            case "light":
                append_to_flavour = "acidic"
            case "medium":
                append_to_flavour = "rounded"
            case "dark":
                append_to_flavour = "bitter"
        self.flavour_impact.append(append_to_flavour)

        self.flavour_impact = list(set(self.flavour_impact))

        
from src.coffee_factory import ExtractionResult
from src.action_object import ActionObject
from game_objects.game_object import Flavour, GameObject
from src.grammar import Grammar
from src.printing import *
from src.state import Physical
from components import Drinkable
from typing import Dict, List
from random import choice
from game_objects.mixture import Mixture

class Product(GameObject):
    def __init__(self, game_instance):
        super().__init__(game_instance)
        self.name = "product"
        self.lore = "This is the liquid you have produced with your very particular recipe and somewhat unique approach."
        self.flavour_impact = []
        self.property = Physical.LIQUID
        self.AddComponent(Drinkable())
        self.register_callable_method(ActionObject("taste", None, False, [self.taste_product]))
        self.fixed_flavours = []
        self.threhold_prominent: float = 0.0
        self.threhold_medium: float = 0.0

    def setup(self, extract: ExtractionResult):
        for flavour in extract.flavors:
            self.add_taste(flavour, 1.0, extract.flavors[flavour])
        self.calculate_thresholds(extract.flavors)

        for name, amount in extract.flavors.items():
            taste_string = self.get_taste_string(name, amount)            
            self.fixed_flavours.append((taste_string, amount))

        self.fixed_flavours.sort(key= lambda item: item[1], reverse=True)

    def taste_product(self):
        complexity = self.get_complexity_string()
        say(f"You take a sip of the {thing(self.name)}. You swirl it around in your mouth, trying to discern the different flavors.")
        say(f"You deem the flavour to be quite ... {complexity}.")
        for flavour_text in self.fixed_flavours:
            say(flavour_text[0])


    def get_taste_string(self, name: str, amount: float) -> str:
        prominent_replies = [
            f"A bold touch of {name} takes center stage in this cup.",
            f"You [italic]really[/italic] enjoy the {name}ness of the product.",
            f"Most prominent is the {name}ness, which reminds you of childhood.",
            f"This might be the most {name} coffee you've had today. Maybe even this week.",
        ]

        mid_replies = [
            f"Really strange how well the {name} components fit into the rest.",
            f"This particular recipe really brings out the {name}ness.",
            f"The {name}ness really wraps up the coffee nicely.",
            f"The balance of {name} and other flavors makes this an exquisite experience.",
        ]

        subtle_replies = [
            f"There is just the slightest {name} hint in the coffee.",
            f"Subtle {name} notes dance on your palate.",
            f"You detect a lingering {name} finish that keeps you coming back for another sip.",
            f"As the coffee cools, the {name}ness becomes slightly more pronounced.",
        ]

        if amount >= self.threhold_prominent:
            return choice(prominent_replies)
        elif amount >= self.threhold_medium:
            return choice(mid_replies)
        else:
            return choice(subtle_replies)

    def get_complexity_string(self):
        res = "simple"
        compexity_scale = [
            "simple",
            "basic",
            "refined",
            "rich",
            "intricate",
            "complex",
            "divine",
            "godly",
            "unfathomable"
        ]
        look_at_index = len(self.taste) - 1
        if len(compexity_scale) >= look_at_index:
            res = compexity_scale[look_at_index]

        return res

    def calculate_thresholds(self, flavours: Dict[str, float]):
        """Calculate threholds based on extract input profile"""
        if not flavours:
            return 0.0, 0.0
        
        intensities = list(flavours.values())
        max_intensity = max(intensities)
        average_intensity = sum(intensities) / len(intensities)
        
        self.threhold_prominent = max_intensity * 0.75
        self.threhold_medium = average_intensity * 0.75


        


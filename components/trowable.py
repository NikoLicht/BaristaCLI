from collections.abc import Callable
from .component import Component
from src.printing import *
from src.grammar import Grammar
from src.action_object import ActionObject
from src.state import Physical
import math

class Throwable(Component):
    def __init__(self, flavour_text = None, callback: Callable = None):
        super().__init__()
        self.add_method(ActionObject("throw", None, methods=[self.throw]))
        self.flavour_text = flavour_text
        self.callback = callback

    def throw(self):
        gr = Grammar()
        if self.owner.has_state("hot"):
            say(f"First of all. Ouch. You burn youself on the very hot {thing(self.owner.name)}.")

        weight = self.owner.get_weight()
        dist = self.calculate_distance_of_throw(weight)
        meters = dist["meters"]
        centi = dist["centimeters"]
        if weight > 18000:
            say(f"You can't really {action("throw")} the {thing(self.owner.name)} with your spaghetti-like arms. It is more like a drop. You manage to {action("throw")} it a whopping {meters} meters and {centi} centimeters.")
        
        else:
            if self.owner.property in [Physical.SOLID, Physical.MUSH]:
                say(f"You think about it. But still decide to {action("throw")} the {thing(self.owner.name)}. I don't really know why.")
                say(f"You manage an astounding {min(meters, 51)} meters and {centi} centimeters.")

            else:
                say(f"You make a mess. Like what did you expect. You are basically throwing {str(self.owner.property.name)} around.")

        if self.callback is not None:
            self.callback()


    
    def calculate_distance_of_throw(self, weight: int) -> dict:
        """Calculates how far a normal person could throw the object
        
        :param weight int: weight in grams
        :return: returns a dict with 'meters' and 'centimeters'"""
    
        g = 9.81  # Gravity (m/s²)
        theta = math.radians(15)  # Convert angle to radians
        
        # Adjusted initial velocity model: decay is less aggressive
        v0 = 25 * math.exp(-0.0001 * weight)  # Adjusted velocity model

        
        # Compute range using projectile motion equation
        range_meters = (v0 ** 2 * math.sin(2 * theta)) / g
        
        # Convert to meters and centimeters
        meters = int(range_meters)
        centimeters = round((range_meters - meters) * 100, 2)
        centimeters = round(centimeters)
        
        return {"meters": meters, "centimeters": centimeters}
        


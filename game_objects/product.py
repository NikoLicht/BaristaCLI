from src.action_object import ActionObject
from game_objects.game_object import GameObject
from src.grammar import Grammar
from src.printing import *
from src.state import Physical
from components import Drinkable
from typing import List
from random import choice
from game_objects.mixture import Mixture

class Product(GameObject):
    def __init__(self, game_instance):
        super().__init__(game_instance)
        self.name = "product"
        self.flavour_impact = []
        self.property = Physical.LIQUID
        self.AddComponent(Drinkable())
        self.register_callable_method(ActionObject("analyze", None, False, [self.analyze]))
        self.register_callable_method(ActionObject("taste", None, False, [self.taste]))

    def setup(self, input: List[GameObject], extraction = 0):
        self.extraction = extraction
        self.input = input if not None else []
        self.flatten_input()
        self.mix_flavours()

    def taste(self):
        complexity = "simple"
        gr = Grammar()
        match(len(self.input)):
            case 1:
                complexity = "stupidly simple"
            case 2:
                complexity = "basic"
            case 3:
                complexity = "balanced"
            case 4:
                complexity = "refined"
            case 5:
                complexity = "rich"
            case 6:
                complexity = "intricate"
            case 7:
                complexity = "masterfully complex"
            case _:
                complexity = "divine"

        say(f"You take a sip of the {thing(self.name)}. You slurp it around in your mouth, trying to discern the different flavors.")
        say(f"You quickly realize that the flavour is quite ... {complexity}. You notice very delicate yet prominent notes of {gr.make_list(self.flavour_impact, "and", req)}.")


    def analyze(self):
        smell = choice(self.input)
        color = choice(self.input)

        say(f"You hold up the {thing(self.position.name)} and take a closer look at it.")
        say(f"The color seems to be very akin to the {thing(color.name)} that you put into it.")
        say(f"The fragrance is very reminiscent of the {thing(smell.name)} that you put into it.")
        say(f"Interesting.")

    def mix_flavours(self):
        for obj in self.input:
            self.flavour_impact.extend(obj.flavour_impact)

    def flatten_input(self):
        all_objects = []
        for obj in self.input:
            if isinstance(obj, Mixture):
                all_objects.extend(obj.in_mixture)
            else:
                all_objects.append(obj)



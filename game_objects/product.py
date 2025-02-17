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
        self.lore = "This is the liquid you have produced with your very particular recipe and somewhat unique approach."
        self.flavour_impact = []
        self.property = Physical.LIQUID
        self.AddComponent(Drinkable())
        self.register_callable_method(ActionObject("analyze", None, False, [self.analyze]))
        self.register_callable_method(ActionObject("taste", None, False, [self.taste]))
        self.fixed_flavours = None

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

        say(f"You take a sip of the {thing(self.name)}. You swirl it around in your mouth, trying to discern the different flavors.")
        say(f"You quickly realize that the flavour is quite ... {complexity}.")
        if self.fixed_flavours is not None:
            for flavour_text in self.fixed_flavours:
                say(flavour_text)
        else:
            self.fixed_flavours = []
            for i in range(3):
                taste = self.get_taste_string(choice(self.flavour_impact))
                say(taste)
                self.fixed_flavours.append(taste)


    def analyze(self):
        smell = choice(self.input)
        color = choice(self.input)

        say(f"You hold up the {thing(self.position.name)} containing the {thing("product")} and take a closer look at it.")
        say(f"The color seems to be very akin to the {thing(color.name)} that you put into it.")
        say(f"The fragrance is very reminiscent of the {thing(smell.name)} that you put into it.")
        say(f"Interesting.")

    def mix_flavours(self):
        for obj in self.input:
            self.flavour_impact.extend(obj.flavour_impact)

    def get_taste_string(self, flavour: str) -> str:
        replies = [
            f"You [italic]really[/italic] enjoy the {flavour}ness of the product.",
            f"Most prominent is the {flavour}ness, which reminds you of childhood.",
            f"{flavour}ness lingers in the mouth afterwards.",
            f"This might be the most {flavour} coffee you've had today. Maybe even this week.",
            f"Really strange how well the {flavour} components fit into the rest.",
            f"There is just the slightest {flavour} hint in the coffee.",
            f"This particular recipe really brings out the {flavour}ness.",
            f"The {flavour}ness really wraps up the coffee nicely.",
            f"A bold touch of {flavour} takes center stage in this cup.",
            f"Subtle {flavour} notes dance on your palate.",
            f"You detect a lingering {flavour} finish that keeps you coming back for another sip.",
            f"The balance of {flavour} and other flavors makes this an exquisite experience.",
            f"A surprising burst of {flavour}ness greets you at first sip, mellowing out as you drink.",
            f"If coffee had a signature move, this one’s would be its {flavour} kick.",
            f"The {flavour} undertones create a depth that keeps you intrigued.",
            f"The coffee surprises you with an unexpected yet pleasant {flavour} twist.",
            f"The {flavour} quality adds a nostalgic touch to the tasting experience.",
            f"You never knew {flavour} could work so well in coffee—until now.",
            f"As the coffee cools, the {flavour}ness becomes even more pronounced."
        ]
        return choice(replies)


    def flatten_input(self):
        all_objects = []
        for obj in self.input:
            if isinstance(obj, Mixture):
                all_objects.extend(obj.in_mixture)
            else:
                all_objects.append(obj)



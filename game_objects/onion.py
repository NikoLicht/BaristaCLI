from components import *
from game_objects import *
from src.printing import *
from src.state import Physical
from src.grammar import Grammar

class Onion(GameObject):
    def __init__(self, game_instance):
        super().__init__(game_instance)
        self.name = "Onion"
        self.property = Physical.SOLID
        self.game_instance = game_instance
        self.flavour_impact = ["tear-inducing"]
        self.lore = "Harvested from the semi-local onion fields in your closest produce producing country."

        self.AddComponent(Edible(f"You force yourself to {action("eat")} the entire {thing(self.name)}. Now you are crying.", on_eat=self.on_eat))
        self.AddComponent(Watchable("It looks appealing somehow. The shape is very bulbous."))
        self.AddComponent(Slapable(f"Very satisfying. The {action("slap")}, it just felt right."))

    def on_eat(self):
        from game_objects import Tears
        say(f"You notice that the {thing("tears")} running down your face land on the counter.")
        self.game_instance.create_new_game_object("tears", Tears) 
        
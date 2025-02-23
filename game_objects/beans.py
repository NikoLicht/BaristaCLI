from .game_object import GameObject, Flavour
from components import *
from src.state import Physical, Temperature
from random import choice

class Beans(GameObject):
    def __init__(self, game_instance):
        super().__init__(game_instance)
        self.name = "beans"
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
        self.start_text = f"Todays beans are a {self.roast} roast from {self.origin_country}."
        self.print_game_text()
        

    def set_origin(self):
        coffee_flavors = {
            "Brazil": {"flavours": [
                Flavour("nut-like", 0.6, 2.0),
                Flavour("chocolatey", 0.7, 4.5),
            ]},
            "Colombia": {"flavours": [
                Flavour("caramel", 0.7, 3.0),
                Flavour("fruity", 0.6, 3.0),
            ]},
            "Ethiopia": {"flavours": [
                Flavour("floral", 0.8, 2.5),
                Flavour("citrus", 0.7, 3.5),
                Flavour("wine", 0.6, 4.0)
            ]},
            "Kenya": {"flavours": [
                Flavour("berry-like", 0.9, 3.0),
                Flavour("bright", 0.8, 4.0),
                Flavour("round", 0.7, 3.5)
            ]},
            "Guatemala": {"flavours": [
                Flavour("chocolatey", 0.7, 4.0),
                Flavour("spicy", 0.6, 3.0),
                Flavour("round", 0.8, 3.5)
            ]},
            "Costa Rica": {"flavours": [
                Flavour("citrus", 0.7, 3.5),
                Flavour("clean", 0.8, 2.0),
            ]},
            "Honduras": {"flavours": [
                Flavour("sweet", 0.7, 2.5),
                Flavour("nutty", 0.6, 3.0),
                Flavour("mild", 0.5, 3.5)
            ]},
            "Mexico": {"flavours": [
                Flavour("chocolatey", 0.6, 4.0),
                Flavour("light", 0.5, 2.0),
                Flavour("nutty", 0.6, 3.0)
            ]},
            "Vietnam": {"flavours": [
                Flavour("bold", 0.8, 4.5),
                Flavour("earthy", 0.7, 3.5),
                Flavour("bitter", 0.6, 4.0)
            ]},
            "Indonesia": {"flavours": [
                Flavour("earthy", 0.7, 3.5),
                Flavour("spicy", 0.6, 3.0),
                Flavour("full", 0.8, 4.0)
            ]},
            "Peru": {"flavours": [
                Flavour("mild", 0.5, 2.0),
                Flavour("nutty", 0.6, 3.0),
                Flavour("chocolatey", 0.6, 4.0)
            ]},
            "India": {"flavours": [
                Flavour("spicy", 0.7, 3.0),
                Flavour("round", 0.8, 4.0),
                Flavour("mellow", 0.5, 2.0)
            ]},
            "Tanzania": {"flavours": [
                Flavour("berry-like", 0.9, 3.0),
                Flavour("bright", 0.8, 3.5),
                Flavour("winey", 0.7, 4.0)
            ]},
            "Rwanda": {"flavours": [
                Flavour("floral", 0.8, 2.5),
                Flavour("fruity", 0.7, 3.0),
                Flavour("tea-like", 0.6, 2.0)
            ]},
            "Yemen": {"flavours": [
                Flavour("spicy", 0.7, 3.0),
                Flavour("winey", 0.8, 4.0),
            ]},
            "Antarctica": {"flavours": [
                Flavour("ice", 0.8, 0.1),
                Flavour("lonelyness", 0.8, 0.1),
            ]}
        }
        self.origin_country = choice(list(coffee_flavors))
        self.coffee_flavour = coffee_flavors[self.origin_country]["flavours"]

        for flavour in self.coffee_flavour:
            self.add_taste(flavour.taste, flavour.solubility, flavour.amount)

        self.roast = choice(["light", "medium", "dark"])
        append_to_flavour = ""
        match(self.roast):
            case "light":
                append_to_flavour = "acidic"
            case "medium":
                append_to_flavour = "rounded"
            case "dark":
                append_to_flavour = "bitter"
        self.add_taste(append_to_flavour, 0.6, 3)

        
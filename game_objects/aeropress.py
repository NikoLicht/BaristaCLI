from .game_object import *
from components import *
from src.grammar import Grammar
from typing import List, Dict
from src.printing import *
from src.state import Physical
from src.action_object import ActionObject

class AeroPress(GameObject):
    def __init__(self, game_instance):
        super().__init__(game_instance)
        self.name = "AeroPress"
        self.weight = 323
        self.register_callable_method(ActionObject("press", "into", False, [self.press], [self]))
        self.AddComponent(Slapable("You knock the AeroPress over, you doof."))
        self.container: Container = self.AddComponent(Container())
        self.AddComponent(Watchable("The suspect seems to have a plastic-like composition."))
        self.AddComponent(Throwable())
        self.flavour_impact = ["Plasticy"]
        self.property = Physical.SOLID

    def press(self, into_target):
        contents: List["GameObject"] = self.container.get_contents([])
        grammar = Grammar()

        if len(contents) == 0:
            say(f"You {action("press")} the empty {thing(self.name)}, nothing comes out of it.")
            return

        sorted_states: Dict["Physical", "GameObject"]= {} 

        for game_object in contents:
            property = game_object.property
            if property in sorted_states:
                sorted_states[property].append(game_object)
            else:
                sorted_states[property] = []
                sorted_states[property].append(game_object)
        
        check_for_hot = sorted_states.get(Physical.LIQUID, []) + sorted_states.get(Physical.MUSH, [])
        if len(check_for_hot) == 0:
            say(f"You do your best, but you cannot {action("press")} a single drop of liquid though.")
            return
        
        emparted_flavours = []
        for obj in contents:
            if obj.flavour_impact:
                emparted_flavours.extend(obj.flavour_impact)

        extraction_level: int = 1 if any(obj.has_state("hot") for obj in check_for_hot) else 0

        say(f"You press the {grammar.make_list(contents)} through the {thing(self.name)}.")

        if len(contents) == 1:
            say(f"But it is essentially still just {thing(contents[0].name)}. Now it is just inside the {thing(into_target.name)}.")
            contents[0].set_position(into_target)
            self.container.clear_contents()
            return

        
        self.game_instance.destroy_game_object(self.container.get_contents([]))
        self.container.clear_contents()

        from .product import Product
        product = self.game_instance.create_new_game_object("product", Product)
        product.setup(contents, extraction_level)
        product.set_position(into_target)
        
        from .puck import Puck
        puck = self.game_instance.create_new_game_object("puck", Puck)
        puck.setup(contents)
        puck.set_position(into_target)



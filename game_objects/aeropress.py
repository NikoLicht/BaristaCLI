from game_objects.mixture import Mixture
from .game_object import *
from components import *
from src.grammar import Grammar
from typing import List, Dict, TYPE_CHECKING
from src.printing import *
from src.state import Physical

if TYPE_CHECKING:
    from src.action_object import ActionObject

class AeroPress(GameObject):
    def __init__(self, game_instance):
        super().__init__(game_instance)
        self.name = "AeroPress"
        self.lore = "An amazing, yet simple, coffee maker, that is somehat a mix between a french-press and a syringe. This is the old model made from some-colored plastic. The numbers are almost not visible anymore."
        self.weight = 323
        self.register_callable_method(ActionObject("press", "into", False, [self.press], [self]))
        self.register_callable_method(ActionObject("wait", None, False, [self.wait], [self]))
        self.AddComponent(Slapable("You knock the AeroPress over, you doof."))
        self.container: Container = self.AddComponent(Container())
        self.AddComponent(Watchable("The suspect seems to have a plastic-like composition."))
        self.AddComponent(Throwable())
        self.add_taste("plastic", 0.03, 2)
        self.property = Physical.SOLID
        self.extraction_time = 0 #1 minute


    def wait(self):
        if len(self.container.contains) == 0:
            say(f"You {action("wait")} for the {thing(self.name)} to extract flavour. Nothing will happen, as it is empty.") 
            return
        self.extraction_time += 1
        say(f"You {action("wait")} for the {thing(self.name)} to extract more flavour. It has brewed for a total of {self.extraction_time} minutes now.")

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
        

        say(f"You press the {grammar.make_list(contents)} through the {thing(self.name)}.")

        contains_mixture = any(isinstance(cont, Mixture) for cont in contents)
        if not contains_mixture and len(contents) == 1:
            say(f"But it is essentially still just {thing(contents[0].name)}. Now it is just inside the {thing(into_target.name)}.")
            contents[0].set_position(into_target)
            self.container.clear_contents()
            return

        #state is: there is now both a liquid and something else in the aeropress 

        #destroying all contents and making puck and product from the remains. Should be refactored
        self.game_instance.destroy_game_object(self.container.get_contents([]))
        self.container.clear_contents()

        from src.coffee_factory import CoffeFactory
        cfactory = CoffeFactory(self.game_instance)
        extraction_result =  cfactory.extract_flavors(contents, self.extraction_time)

        #for key, val in extraction_result.flavors.items():
            #print(f"    extraction of {key}ness - {round(val, 2)}.")

        #print(cfactory.get_waste_flavours(extraction_result))

        cfactory.create_product(extraction_result, into_target)
        cfactory.create_puck(extraction_result, self)




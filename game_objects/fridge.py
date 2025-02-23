from game_objects import *
from components import *
from src.printing import *
from src.state import Physical, Temperature
from src.action_object import ActionObject  
from random import choice

#something is not working with the cration of objects in the game class, meaning the command open fridge - > watch fridge does something terrible?
#perhaps an endless loop.
class Fridge(GameObject):
    def __init__(self, game_instance):
        super().__init__(game_instance)
        self.name = "fridge"
        self.weight = 102000
        self.spelled_word = choice(["F R I D G E", "B U T T E R", "S A D", "B E A N S", "S U D O"])
        self.lore = f"Nice pistacchio-colored retro fridge from the brand SMEG. You've had it for a while. Upon it hangs a few magnetic letters spelling out {self.spelled_word}."
        self.register_callable_method(ActionObject("open", None, False, [self.open], [self]))
        self.watch: Watchable = self.AddComponent(Watchable("You wonder what mysteries it contains. You also wonder about the humming sound it makes."))
        self.AddComponent(Throwable())
        self.has_watched = False
        self.container: Container = self.AddComponent(Container())
        self.add_taste("refrigerant", 0.7, 7)
        self.add_taste("electronic", 0.4, 3)
        self.property = Physical.SOLID
        self.add_state(Temperature.COLD)


    def open(self):
        say(f"You {action("open")} the {thing("fridge")} door. As usual, the hinges make that little squeek when the door is almost open.")
        
        #handle watch the open fridge
        self.watch.flavour_text = "You look inside the fridge and realize that you have a few things in there as well."
        self.watch.on_watch = self.on_watch

    
    def on_watch(self):
        if not self.has_watched:
            self.has_watched = True

            from game_objects import Ketchup
            ketchup = self.game_instance.create_new_game_object("ketchup", Ketchup)
            ketchup.position = self
            self.container.contains.append(ketchup)

            from game_objects import Onion
            onion = self.game_instance.create_new_game_object("onion", Onion)
            onion.position = self
            self.container.contains.append(onion)


     
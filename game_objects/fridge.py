from game_objects import *
from components import *
from src.printing import *
from src.state import Physical


class Fridge(GameObject):
    def __init__(self, game_instance):
        super().__init__(game_instance)
        self.name = "fridge"
        self.register_callable_method("open", self.open)
        self.watch: Watchable = self.AddComponent(Watchable("You wonder what mysteries it contains. You also wonder about the humming sound it makes."))
        self.has_watched = False
        self.container: Container = self.AddComponent(Container())
        self.flavour_impact = ["refrigerant", "electronics"]
        self.property = Physical.SOLID

    def open(self):
        say(f"You {action("open")} the {thing("fridge")} door. As usual, the hinges make that little squeek when the door is almost open.")
        
        #handle watch the open fridge
        self.watch.flavour_text = "You look inside the fridge and realize that you have a few things in there as well."
        self.watch.on_watch = self.on_watch

    
    def on_watch(self):
        if not self.has_watched:
            self.has_watched = True
            ketchup = self.game_instance.create_new_game_object("ketchup", Ketchup)
            ketchup.position = self
            self.container.contains.append(ketchup)


     
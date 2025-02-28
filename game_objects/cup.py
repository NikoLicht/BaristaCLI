from components import *
from game_objects import *
from src.printing import *
from src.state import Physical
from src.grammar import Grammar
from src.action_object import ActionObject


class Cup(GameObject):
    def __init__(self, game_instance):
        super().__init__(game_instance)
        self.name = "cup"
        self.property = Physical.SOLID
        self.add_taste("gravel", 0.3, 5)
        self.game_instance = game_instance
        self.weight = 421
        self.lore = "This is a double-walled ceramic thermo Loveramics Nomad mug, holding approximatly 250ml. In the color taupe. Very nice."

        self.AddComponent(Watchable(f"One of your favourite cups. You really love this {thing(self.name)}, that your grandmother gave you."))
        self.AddComponent(Slapable("[italic]Why did I just do that[/ italic]- you think.", self.break_cup))
        self.AddComponent(Throwable())
        self.container: Container = self.AddComponent(Container())
        self.register_callable_method(ActionObject("swirl", None, False, [self.swirl], [self]))

    def break_cup(self):
        say(f"The {thing(self.name)} breaks into 43 porcelain pieces which now lie on your floor. Watch your step.")
        self.game_instance.destroy_game_object([self])

    def swirl(self):
        if self.property is not Physical.SOLID:
            say(f"You attempt to {action("swirl")} the cup around, but as it is now basically {self.property} you have hard time.")
            return
        gr = Grammar()
        then = "" 
        cup_contents = self.container.contains
        if len(cup_contents) == 0:
            then = f"The {thing(self.name)} is empty, so you feel a bit stupid doing this."
        else:
            then = f"The {gr.make_list(cup_contents)} swirl around. You feel very fancy doing this. You, and James Hoffman, are not really sure if it does anything."
        say(f"You {action("swirl")} the {thing(self.name)} around. {then}")
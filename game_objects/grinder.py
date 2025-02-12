from components import *
from src.grammar import Grammar
from game_objects import *
from src.printing import *
from src.state import Physical, Verbs

class Grinder(GameObject):

    def __init__(self, game_instance):
        super().__init__(game_instance)
        self.name = "grinder"
        self.lore = "The new super premium Commandante, what a delicious mechanical feel it has. It can fit surprisingly much."
        self.container: Container = self.AddComponent(Container())
        self.AddComponent(Crankable(self.grind))
        self.AddComponent(Watchable("It bears marks of use, like a warriors armor."))
        self.AddComponent(Slapable("Ouch! The metal grinder leaves an imprint on your hand. It is also knocked over."))
        self.flavour_impact = ["Metallic"]
        self.property = Physical.SOLID

    def grind(self):
        grinder_content = self.container.get_contents([])
        make_mixture: bool = len(grinder_content) > 1

        if make_mixture:
            grammar = Grammar()
            if self.container:
                grinder_content_str = grammar.make_list(grinder_content)
                say(f"You grind {grinder_content_str} into a coarse {thing("mixture")}.")

                #Transform states
                for obj in grinder_content:
                    if obj.property is Physical.SOLID:
                        obj.change_property(Physical.SAND)

                
                self.contains_mixture(grinder_content)

        else:
            single_object = grinder_content[0]
            single_object_state = grinder_content[0].property

            if single_object_state is Physical.SOLID:
                say(f"You grind the {thing(single_object.name)} into a sand-like state.")
                single_object.change_property(Physical.SAND)
            else:
                say(f"You grind the {thing(single_object.name)}, but nothing happens, because it is a {single_object_state.name.lower()}.")


    def contains_mixture(self, grinder_content: list):
        from .mixture import Mixture
        mixture = next((x for x in grinder_content if isinstance(x, Mixture)), None)
        if mixture:
            grinder_content.remove(mixture)
        else:
            mixture = self.game_instance.create_new_game_object("mixture", Mixture)
            self.container.contains = [mixture]

        self.game_instance.destroy_game_object(grinder_content)
        mixture.mix(*grinder_content)

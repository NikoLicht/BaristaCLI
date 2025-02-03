from .game_object import GameObject
from components import *
from typing import TypeVar, List
from src.printing import *
from src.state import Physical
from src.grammar import Grammar
T = TypeVar("T", bound=GameObject)

class Mixture(GameObject):
    def __init__(self, game_instance, *args: T):
        super().__init__(game_instance)
        self.name = "mixture"
        self.in_mixture = []
        self.flavour_impact = []
        self.property = None

    def mix(self, *args: T):
        for obj in args:
            #Record what is in mixture
            if not obj.__getattribute__("name"):
                print(obj)

            #Add components
            for component_key in obj._components:
                if component_key not in self._components:
                    self.AddComponent(obj._components[component_key])

            #Add states
            self._state_list.extend(obj._state_list)
            
            #object position should be the same for all objects
            self.position = obj.position

            #add flavour
            self.flavour_impact.extend(obj.flavour_impact)

            #add composition
            self.in_mixture.append(obj)

        
        self._mix_properties([x.property for x in args])

        #override components
        slap: Slapable= self.get_component("slapable")
        if slap:
            match(self.property):
                case Physical.LIQUID:
                    slap.flavour_text = "Bits of mushy mess flies all over the kitchen."
                case Physical.GAS:
                    slap.flavour_text = "Actually you can't really slap a gas."
                case Physical.MUSH:
                    slap.flavour_text = "A loud squishy slap sound appears. Extremely satisfying."
                case Physical.SOLID:
                    slap.flavour_text = "This is indeed a very solid object. Your hand- and feelings hurt."
                case Physical.SAND:
                    slap.flavour_text = "A big poof of dust emerges from the kithcen table. Reminiscent of a magic show."

        watch: Watchable = self.get_component("watchable")
        if watch:
            match(self.property):
                case Physical.LIQUID:
                    watch.flavour_text = "Indeed a strangely mesmerizing liquid."
                case Physical.GAS:
                    watch.flavour_text = "Probably easier to smell, than to watch."
                case Physical.MUSH:
                    watch.flavour_text = "A gooey mixture. Almost a turd-like apperance."
                case Physical.SOLID:
                    watch.flavour_text = "The surface almost has an egg-shell-like texture to it. Almost."
                case Physical.SAND:
                    watch.flavour_text = "A dusty lump of tiny particles. Perfect for you vacuum cleaner. Terrible for your allergies."

        container: Container = self.get_component("container")
        if container:
            container.contains = []

    def _mix_properties( self, properties: List[Physical]):
        properties.append(self.property)

        #if all properties are the same
        if all(property == properties[0] for property in properties):
            self.property = properties[0]
            return
        
        if all(property in [Physical.SAND, Physical.SOLID] for property in properties):
            self.property = Physical.SAND
            return

        if Physical.LIQUID in properties or Physical.MUSH in properties:
            self.property = Physical.MUSH
            return

        self.property = Physical.MUSH

    def status(self):
        super().status()
        if len(self.in_mixture) > 0:
            gr = Grammar()
            say(f"{thing(self.name)} is composed of {gr.make_list(self.in_mixture)}.")    




    
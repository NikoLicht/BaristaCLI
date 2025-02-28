from .component import Component
from src.grammar import Grammar
from typing import TYPE_CHECKING, List
from src.printing import *
from src.action_object import ActionObject
if TYPE_CHECKING:
    from game_objects import *


class Container(Component):
    def __init__(self):
        super().__init__()
        self.contains: List[GameObject] = []
        self.add_method(ActionObject("empty", None, methods=[self.empty]))
        self.register_required_word("into")

    def fill(self, content, triggered_action = False) -> None:
        """Puts content into this container.
        
        :param content GameObject: the content to add
        :param triggered_action bool: is it triggered externally (not by player)"""
        self.contains.append(content)
        former_container_obj = content.position

        if former_container_obj:
            former_container: Container = former_container_obj.get_component("container")
            if former_container:
                former_container.remove_content(content)

        content.position = self.owner
        if not triggered_action:
            say(f"You {action("put")} the {thing(content.name)} {req("into")} the {thing(self.owner.name)}.")
            return
        say(f"You also {action("put")} the {thing(content.name)} {req("into")} the {thing(self.owner.name)}. Because the {thing(former_container_obj.name)} contained it")

    def empty(self):
        """The 'empty' action, has print output."""
        if len(self.contains) <= 0:
            say(f"There is nothing in the {thing(self.owner.name)} ... yet. You cannot {action("empty")} it.")
        else:
            grammar = Grammar()
            say(f"You remove the {grammar.make_list(self.contains)} from the {thing(self.owner.name)}.")
            for obj in self.contains:
                obj.position = None
            self.clear_contents()

    def clear_contents(self):
        """Empties container"""
        self.contains.clear()

    def remove_content(self, content):
        """Remove specific item from contents"""
        if content in self.contains:
            self.contains.remove(content)

    #TODO: maybe rework this to be general purpose?
    def recursive_action(self, action: str, arg):
        """Tries to call same action on all contents"""
        for object in self.contains:
            object.try_call_method(action, arg)

    def status(self):
        """Container specific status fuction"""
        grammar = Grammar()
        if len(self.contains) > 0:
            say(f"{thing(self.owner.name)} contains {grammar.make_list(self.contains)}.")

    def get_contents(self, discovered_items: List) -> List["GameObject"]:
        """
        Recusively gets all nested gameobjects as a flattened list.

        :param str discovered_itemes: initally an empty list that gets passed on to each call 
        """
        for content in self.contains:
            if content not in discovered_items:
                discovered_items.append(content)
                child_container = content.get_component("container")
                if child_container:
                    child_container.get_contents(discovered_items)

        return discovered_items


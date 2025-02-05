import os
from typing import TYPE_CHECKING, List

from .command import Command
from .grammar import Grammar
from .printing import *
from sys import exit
from rich.console import Console
import time

if TYPE_CHECKING:
    from game import Game



class CLI():
    def __init__(self):
        self.game_instance : "Game" = None
        self.single_word_actions = ["exit", "quit", "help", "objects", "actions", "actions-all"]

    def set_game(self, set_game):
        self.game_instance = set_game

    def execute_command(self, command: Command):
        #print(str(command))

        if command is None:
            return
        
        if command.is_single_command():

            if command.action in self.single_word_actions:

                self.execute_single_command(command.action)
                return
        
            if command.action in self.game_instance.objects:
                self.game_instance.objects[command.action].try_call_method("status")
                return
            
        for obj in command.input_objects:
            if command.required_parameter is not None:
                #print(f"Performing complex action {command.action} on {obj.name} and {command.target.name}")
                self.game_instance.perform_action_complex(command.action, obj, command.target)
            else:
                #print(f"Performing simple action {command.action} on {obj.name}")
                self.game_instance.perform_action_simple(command.action, obj)

    def parse_command(self, input: str) -> Command:
        command: Command = Command()
        words = [x for x in input.split() if x != "and"]
        if len(words) == 1:
            if words[0] in self.single_word_actions:
                command.action = words[0]
                return command
            if words[0] in self.game_instance.objects:
                command.action = words[0]
                return command
            else:
                warn(f"I don't know that action - see {action('actions')} for a list of actions.")
                return None
        if self.help_check(words):
            return None

        command.action = words[0]
        if command.action not in self.game_instance.registered_actions and command.action not in self.single_word_actions and command.action not in self.game_instance.objects:
            warn(f"I don't know that action yet - see {action('actions')} for a list of actions.")
            return None
        
        if command.action not in self.game_instance.registered_actions:
            warn(f"I don't know that action yet - see {action('actions')} for a list of actions.")
            return None
        action_obj = self.game_instance.registered_actions[command.action]
        if action_obj.required_parameter is not None:
            target_key = words[-1]
            command.required_parameter = words[-2]
            if command.required_parameter != action_obj.required_parameter: 
                warn(f"{action(command.action)} requires that you use {action_obj.required_parameter} - see {action('help')} {thing(command.action)} for usage.")
                return None
            if target_key not in self.game_instance.objects:
                warn(f"I don't know of any object {thing(target_key)} - see {action('objects')} for a list of objects.")
                return None

            command.target = self.game_instance.objects[target_key]            

        #Take input between action and required_parameter if there is a required_parameter, else take all input after action
        object_keys = []
        if command.required_parameter:
            object_keys = words[1:-2]
        else:
            object_keys = words[1:]


        command.input_objects = []
        for key in object_keys:
            if key not in self.game_instance.objects:
                warn(f"I don't know of any object [italic]key[/italic] - see {action('objects')} for a list of objects.")
                return None
            command.input_objects.append(self.game_instance.objects[key])


        if action_obj.allows_list is False and len(command.input_objects) > 1:
            warn(f"{action(command.action)} does not list input - see {action('help')} {thing(command.action)} for usage.")
            return None
        
        if command.required_parameter is not None and target_key is not None:
            if command.target.supports_required_word(command.required_parameter) is False:
                warn(f"{thing(target_key.name)} does not support {command.required_parameter} -  see {action('help')} {thing(command.action)} for usage.")
                return None
        
        return command

    def help_check(self, input: List[str]) -> bool:
        if len(input) == 2:
            if "help" in input:
                key = [x for x in input if x != "help"][0]
                if key in self.game_instance.registered_actions:
                    self.game_instance.registered_actions[key].help()
                    return True
                if key in self.game_instance.objects:
                    self.game_instance.objects[key].try_call_method("actions")
                    return True
        return False

                
    def execute_single_command(self, command):
        grammar = Grammar()
        match command:
            case "exit" | "quit":
                say(f"{barista("Bye! See you tomorrow!")}")
                time.sleep(3)
                exit(0)

            case "help":
                say(
                    f"You are the {barista()} in this command line coffe brewing experience",
                    f"You interact by typing {action("actions")} and {thing("objects")} into the command line.",
                    f"Use the action {action("objects")} to see all available interactable {thing("objects")}.",
                    f"To see what {action("actions")} are available on a specific {thing("object")} type: {action("actions")} {thing("object")} eg. {action("actions")} {thing("water")}",
                    f"The {action("put")} action is special, and requires a special grammar: {action("put")} {thing("water")} into {thing("kettle")}", 
                    f"Funnily enough, the goal is to brew a coffee. Good luck, {barista()}.",
                )

            case "objects":
                all_objects: str = grammar.make_list(list(self.game_instance.objects.keys()))
                say(f"The {action("objects")} you have available are: {all_objects}")

            case "actions":
                say(
                    f"There are a few general actions that will get you started:",
                    f"{action("help")} - to get more info about it all.",
                    f"{action("objects")} - to list all objects.",
                    f"{action("actions")} - to list basic actions.\n",
                    f"And then a few actions you do to {thing("objects")}:",
                    f"{action("status")} {thing("object")} - to see the current state of the object.",
                    f"{action("actions")} {thing("object")} - to see what special actions you can do on that object."
                    )
                
            case "actions-all":
                for key, action_obj in self.game_instance.registered_actions.items():
                    say(f"{key} - {str(action_obj)}")

            case _:
                warn("I don't recognize that command. Contact the developer, if you feel in your heart that it should be added.")

    
    def styled_input(self, prompt):
        console = Console()
        user_input = console.input(prompt)  # Get user input

        return user_input  # Return the raw input for processing

    def run(self):
        say(
            f"Welcome to {barista("BaristaCLI")} a virtual coffee bar, where you make your own coffee.",
            f"    {action("quit")} - to leave your job as barista.",
            f"    {action("help")} - to get more info about it all.",
            f"    {action("objects")} - to list all objects.",
            "What do you want to do?",
            )

        while True:
            command = self.styled_input(barista("barista >  "))
            parsed_command = self.parse_command(command)
            self.execute_command(parsed_command)


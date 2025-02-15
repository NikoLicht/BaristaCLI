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
                self.game_instance.objects[command.action].explanation()
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
        input = input.replace(",", "")
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
                warn(f"I don't know of any object [italic]{key}[/italic] - see {action('objects')} for a list of objects.")
                return None
            command.input_objects.append(self.game_instance.objects[key])


        if action_obj.allows_list is False and len(command.input_objects) > 1:
            warn(f"{action(command.action)} does not list input - see {action('help')} {thing(command.action)} for usage.")
            return None
        
        if command.required_parameter is not None and target_key is not None:
            if command.target.supports_required_word(command.required_parameter) is False:
                warn(f"{thing(target_key)} does not support {req(command.required_parameter)} -  see {action('help')} {thing(command.action)} for usage.")
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
                self.log_command_to_file("exit")
                self.log_command_to_file("-------------------------")
                time.sleep(3)
                exit(0)

            case "help":
                say(f"{header("Help!")}")
                say(
                    f"You are the {barista()} in this command line coffee brewing experience",
                    f"You interact by using {action("actions")} on {thing("objects")}. You do this by typing here in your terminal.",
                    f"- Use {action("objects")} to see all available {thing("objects")}.",
                    f"- Use {action("actions")} to get more info about actions.",
                    f"- Use {action("actions")} {thing("object")} to see actions for [italic]that[/italic] object eg. {action("actions")} {thing("water")}.",
                    f"- Some actions like {action("put")} are more complex and require a grammar like: {action("put")} {thing("water")} {req("into")} {thing("kettle")}.", 
                    f"     - You can find out more about a specific action by typing {action("help")} {action("action")} eg. {action("help")} {thing("put")}.", 
                )

            case "objects":
                all_objects: str = grammar.make_list(list(self.game_instance.objects.keys()))
                say(f"{header("Objects")}")
                say(f"The {thing("objects")} you have available are: {all_objects}")

            case "actions":
                say(f"{header("Actions")}")
                say(
                    f"   [u]General actions:[/u]",
                    f"   {action("help")} - to get more info about it all.",
                    f"   {action("objects")} - to list all objects.",
                    f"   {action("actions")} - to list basic actions.",
                    f"   {action("quit")} - to quit",
                    f"",
                    f"   [u]Object Actions:[/u]",
                    f"   And then a few actions you do to {thing("objects")}:",
                    f"   {action("status")} {thing("object")} - to see the current state of the object.",
                    f"   {action("actions")} {thing("object")} - to see the actions you can do to [italic]that[/italic] object.",
                    f"   {action("put")} {thing("object")} into {thing("object")} - to put an object inside another object (that supports it)."
                    )
                
            case "actions-all":
                for key, action_obj in self.game_instance.registered_actions.items():
                    say(f"[u]{action(key)} action object                                         [/u]")
                    say(str(action_obj))

            case _:
                warn("I don't recognize that command. Contact the developer, if you feel in your heart that it should be added.")

    
    def styled_input(self, prompt):
        console = Console()
        user_input = console.input(prompt)  # Get user input

        return user_input  # Return the raw input for processing
    
    def log_command_to_file(self, command):
        with open("commands.log", "a") as file:
            file.write(command + "\n")

    def run(self):
        title("Barista CLI") 
        say(
            f"Welcome to {barista("Barista CLI")} a virtual coffee bar, where you make your own coffee.",
            f"    {action("quit")} - to leave your job as barista.",
            f"    {action("help")} - to get more info about it all.",
            f"    {action("objects")} - to list all objects.",
            f"    {action("actions")} - for more about interacting.",
            "What do you want to do?",
            )

        while True:
            command = self.styled_input(barista("barista >  "))
            parsed_command = self.parse_command(command)
            if parsed_command is not None:
                self.log_command_to_file(command)
            self.execute_command(parsed_command)


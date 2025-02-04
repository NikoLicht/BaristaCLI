import os
from typing import TYPE_CHECKING, List
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

    def set_game(self, set_game):
        self.game_instance = set_game

    def parse(self, sentence):
        seperate_words = sentence.split()

        if len(seperate_words) == 1:
            self.parse_single_command(seperate_words[0])
            return

        if len(seperate_words) == 2:
            first_object = seperate_words[1]
            action = seperate_words[0]
            self.game_instance.perform_action_simple(action, first_object)

        elif seperate_words[2] in ["into", "in"]:
            action = seperate_words[0]
            first_object = seperate_words[1]
            second_object = seperate_words[3]
            self.game_instance.perform_action_complex(action, first_object, second_object)
        else:
            warn("Sorry, but I don't quite understand.")

    def pre_parse_input(self, input: str):
        #find action
        #find out if input contains list
        #check if action supports list_input
        #if not, return error
        #check if action has required_parameter and if the parameter is in the input
        #if yes, find all inputs in list (will be all words seperated by "," and "and")
            #if there is a requried_parameter in the action, the input list will end at that point
        #Then comes the part im unsure about, I have to check if the target of the required_paramter supports the required_action
        #then, in another function, probably execute the action on the list of targets, taking into account the required paramter

        #example: put water, beans, grinder into kettle
        #action: put
        #required_parameter: into
        #list_input: True
        #list: water, beans, grinder
        #target: kettle

        #should probably return an object with all the information, so that the next function can use it

        words = [x for x in input.split() if x != "and"]
        self.help_check(words)
        action = words[0]
        if action not in self.game_instance.registered_actions:
            warn("Action not recognized.")
            return None
        
        action_obj = self.game_instance.registered_actions[action]
        target = None
        required_parameter = None
        if action_obj.required_parameter is not None:
            target = words[-1]
            required_parameter = words[-2]
            if required_parameter != action_obj.required_parameter: 
                warn(f"Action {action} requires {action_obj.required_parameter} as a parameter.")
                return None
            if target not in self.game_instance.objects:
                warn(f"Target {target} not recognized.")
                return None

            target = self.game_instance.objects[target]            

        #Take input between action and required_parameter if there is a required_parameter, else take all input after action
        input_objects = []
        if required_parameter:
            input_objects = words[1:-2]
        else:
            input_objects = words[1:]

        if action_obj.allows_list is False and len(input_objects) > 1:
            warn(f"Action {action} does not support multiple objects.")
            return None
        
        return {
            "action" : action,
            "input_objects" : input_objects,
            "required_parameter" : required_parameter,
            "target" : target,
        }


    def help_check(self, input: List[str]):
        if len(input) == 2:
            if "help" in input:
                key = [x for x in input if x != "help"][0]
                if key in self.game_instance.registered_actions:
                    self.game_instance.registered_actions[key].help()
                

        


    def parse_single_command(self, command):
        grammar = Grammar()
        match command:
            case "exit" | "quit":
                say("Bye! See you tomorrow!")
                time.sleep(4)
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
            print(self.pre_parse_input(command))
            self.parse(command)


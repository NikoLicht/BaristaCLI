import os
from typing import TYPE_CHECKING
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

            case _:
                warn("I don't recognize that command. Contact the developer, if you feel in your heart that it should be added.")

    
    def styled_input(self, prompt):
        console = Console()
        user_input = console.input(prompt)  # Get user input

        return user_input  # Return the raw input for processing

    def run(self):
        say(
            "Welcome to BaristaCLI a virtual coffee bar, where you make your own coffee.",
            f"    {action("quit")} - to leave your job as barista.",
            f"    {action("help")} - to get more info about it all.",
            f"    {action("objects")} - to list all objects.",
            "What do you want to do?",
            )

        while True:
            command = self.styled_input(barista("barista >  "))
            self.parse(command)


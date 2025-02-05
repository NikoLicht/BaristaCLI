from game_objects.game_object import GameObject
from typing import List

class Command():
    def __init__(self):
        self.action: str = None
        self.input_objects: List[GameObject] = None
        self.required_parameter: str = None
        self.target: GameObject = None

    def is_single_command(self) -> bool:
        return self.required_parameter is None and self.target is None and self.input_objects is None
    
    def __str__(self):
        return f"{self.action} - {"No objects" if self.input_objects == None else [obj.name for obj in self.input_objects]} - {self.required_parameter} - {self.target}"
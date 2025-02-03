from .printing import *
class Grammar():
    def __init__(self):
        pass
    
    def make_list(self, input, seperator = "and", style = thing) -> str:
        
        if not isinstance(input, list):
            print("input is not a list!")

        if all(hasattr(item, 'name') for item in input):
            input = [item.name for item in input]

        if not all(isinstance(item, str) for item in input):
            raise ValueError("Input must be a list of strings or objects with a 'name' attribute.")
        
            
        input = [style(obj) for obj in input]
        input = list(set(input))

        return f" {seperator} ".join([", ".join(input[:-1]), input[-1]] if len(input) > 2 else input)

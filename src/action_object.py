from .printing import *
class ActionObject:
    def __init__(self, name: str, required_parameter: str, allows_list: bool = False):
        self.name = name.lower()
        self.required_parameter = None if required_parameter == "None" else required_parameter
        self.allows_list = allows_list

    def __eq__(self, other):
        return isinstance(other, ActionObject) and self.name == other.name
    
    def __hash__(self):
        return hash(self.name)
    
    def __str__(self):
        return f"{self.name} - {self.required_parameter} - {self.allows_list}"
    
    def help(self):
        req_param: bool = self.required_parameter is not None
        multi: bool = self.allows_list
        explanation = f"   With this action, you can {action(self.name)} a single object{"" if not multi else f" or multiple objects"}{"" if not req_param else f" {req(self.required_parameter)} a target object"}"
        explanation += "."

        say(f"   [u]{action(self.name)} help             [/u]")
        say(explanation)
        if self.allows_list:
            if self.required_parameter is not None:
                say(f"   Example: {action(self.name)} {thing('water')}, {thing('beans')} and {thing('cup')} {req(self.required_parameter)} {thing('grinder')}")
            else:
                say(f"   Example: {action(self.name)} {thing('water')}, {thing('beans')} and {thing('cup')}")
        else:
            if self.required_parameter is not None:
                say(f"   Example: {action(self.name)} {thing('water')} {req(self.required_parameter)} {thing('grinder')}")
            else:
                say(f"   Example: {action(self.name)} {thing('water')}")
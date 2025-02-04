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
        say(f"Action: {action(self.name)}")
        req_param_ending = "." if self.required_parameter is None else f" [italic]{self.required_parameter}[/ italic] a target {thing("object")}"
        say(f"   With this action, you can {action(self.name)} a single object{"." if not self.allows_list else f" or multiple objects{req_param_ending}"}")
        if(self.required_parameter is not None):
            say(f"   The action requires a {self.required_parameter} as a parameter.")
        if self.allows_list:
            if self.required_parameter is not None:
                say(f"   Example: {action(self.name)} {thing('water')}, {thing('beans')} and {thing('cup')} {self.required_parameter} {thing('grinder')}")
            else:
                say(f"   Example: {action(self.name)} {thing('water')}, {thing('beans')} and {thing('cup')}")
        else:
            if self.required_parameter is not None:
                say(f"   Example: {action(self.name)} {thing('water')} {self.required_parameter} {thing('grinder')}")
            else:
                say(f"   Example: {action(self.name)} {thing('water')}")
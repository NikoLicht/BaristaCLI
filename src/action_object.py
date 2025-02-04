class ActionObject:
    def __init__(self, name: str, required_parameter: str, allows_list: bool = False):
        self.name = name.lower()
        self.required_parameter = required_parameter
        self.allows_list = allows_list

    def __eq__(self, other):
        return isinstance(other, ActionObject) and self.name == other.name
    
    def __hash__(self):
        return hash(self.name)
    
    def __str__(self):
        return f"{self.name} - {self.required_parameter} - {self.allows_list}"
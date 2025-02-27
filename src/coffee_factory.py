from src.state import Temperature
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from game_objects.game_object import GameObject
    from .game_objects import *
    from game_objects.puck import Puck
    from game_objects.product import Product
    


class ExtractionResult:
    def __init__(self):
        self.flavors: Dict[str, float] = {}

    def __add__(self, other):
        joined_flavours: Dict[str, float] = self.flavors
        for flavour_key in other.flavors:
            if flavour_key in joined_flavours:
                joined_flavours[flavour_key] += other.flavors[flavour_key]
            else: 
                joined_flavours[flavour_key] = other.flavors[flavour_key]
        res = ExtractionResult()
        res.flavors = joined_flavours
        return res
    

class CoffeFactory():

    def __init__(self, game_instance):
        self.game_instance = game_instance

    def calculate_average_temperature(self, extract_from: list["GameObject"]):
        temperature = 0.5
        step_size = 1.0 / float(len(extract_from))

        for ing in extract_from:
            if ing.has_state(Temperature.HOT):
                temperature += step_size
            if ing.has_state(Temperature.COLD):
                temperature -= step_size
        return  temperature


    def create_product(self, extract: ExtractionResult, target_position) -> "Product":
        from game_objects.product import Product
        product: "Product" = self.game_instance.create_new_game_object("product", Product)
        product.setup(extract)
        product.set_position(target_position)
        return product

    def create_puck(self, extract: ExtractionResult, target_position) -> "Puck":
        from game_objects.puck import Puck
        puck: Puck = self.game_instance.create_new_game_object("puck", Puck)
        waste_extract = self.get_waste_flavours(extract)
        puck.setup(waste_extract)
        puck.set_position(target_position)
        return puck

    def get_waste_flavours(self, extract: ExtractionResult) -> ExtractionResult:
        total_extraction_level = sum(extract.flavors.values())
        average_extraction_level = total_extraction_level / len(extract.flavors)
        waste = {flavour: extract.flavors[flavour]*1.5 for flavour in extract.flavors if extract.flavors[flavour] > average_extraction_level}
        return waste


    def map_temperature(self, value: float) -> Temperature:
        """Map a float value (0.0 to 1.0) to a WaterTemperature enum."""
        temp_values = list(Temperature)
        index = int(value * len(temp_values))
        index = min(index, len(temp_values) - 1)  # Ensure index is within range
        return temp_values[index]


    def extract_flavors(self, extract_from: list["GameObject"], time_in_minutes: int) -> ExtractionResult:
        """Determines the extracted flavors and their intensities."""
        extraction = ExtractionResult()
        average_temp: Temperature = self.calculate_average_temperature(extract_from)
        for game_obj in extract_from:
            extraction += game_obj.extract_flavour(average_temp, time_in_minutes)

        return extraction
        
    

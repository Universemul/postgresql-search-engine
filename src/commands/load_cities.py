import json
from dataclasses import dataclass
from typing import List


@dataclass
class City:
    id: int
    department_code: str
    insee_code: str
    zip_code: str
    name: str
    slug: str
    gps_lat: float
    gps_lng: float


class CityEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


def load_file() -> List[City]:
    _file = "../assets/cities.json"
    with open(_file, "r") as f:
        data = json.load(f)
        result = [City(**city) for city in data]
    return result


def init_db(cities: List[City]):
    """
    - Initialize our database
    - Drop table if exists
    - Create table with tsvector
    - Create index on index
    """
    print(cities[0])


if __name__ == "__main__":
    loaded_cities = load_file()
    init_db(loaded_cities)

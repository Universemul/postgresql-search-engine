import json
from dataclasses import dataclass
from typing import List

import psycopg2
from unidecode import unidecode

TABLE = "full_search"
DB_NAME = "test_search"


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


def remove_accents(input_str: str) -> str:
    return unidecode(input_str)


def init_db(cities: List[City]):
    print("START INSERT")
    conn = psycopg2.connect(
        f"dbname='{DB_NAME}' user='postgres' host='localhost' password='postgres'"
    )
    cur = conn.cursor()

    # DROP AND CREATE THE SEARCH TABLE
    cur.execute(f"DROP TABLE IF EXISTS {TABLE}")
    cur.execute(f"CREATE TABLE {TABLE} (id SERIAL, name Text, normalize_name Text)")

    # FORMAT THE CITIES BEFORE INSERTING IN THE DATABASE
    cities_dict = [
        {"id": x.id, "name": x.name, "normalize_name": remove_accents(x.name.lower())}
        for x in cities
    ]
    cur.executemany(
        f"INSERT INTO {TABLE}(id,name,normalize_name) VALUES (%(id)s, %(name)s, %(normalize_name)s)",
        cities_dict,
    )

    cur.execute(
        f"""
        ALTER TABLE {TABLE}
        ADD COLUMN search tsvector
        GENERATED ALWAYS AS  (
            to_tsvector('french', normalize_name)
        ) stored;
    """
    )
    # CREATE INDEX
    cur.execute(f"CREATE INDEX city_idx ON {TABLE} USING GIN (search)")
    # SAVE THE INSERTS
    conn.commit()
    print("INSERT DONE")


if __name__ == "__main__":
    loaded_cities = load_file()
    init_db(loaded_cities)

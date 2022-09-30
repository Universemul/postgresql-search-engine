import json
from dataclasses import dataclass
from typing import List

import psycopg2

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


def init_db(cities: List[City]):
    print("START INSERT")
    conn = psycopg2.connect(
        f"dbname='{DB_NAME}' user='postgres' host='localhost' password='postgres'"
    )
    cur = conn.cursor()

    # DROP AND CREATE THE SEARCH TABLE
    cur.execute(f"DROP TABLE IF EXISTS {TABLE}")
    cur.execute(f"CREATE TABLE {TABLE} (id SERIAL, name Text, search_field TSVECTOR)")

    # CREATE INDEX
    cur.execute(f"CREATE INDEX city_idx ON {TABLE} USING GIN (search_field);")

    # ADD TRIGGER TO AUTOMATICALLY CREATE THE TS_VECTOR
    cur.execute(
        f"""CREATE TRIGGER city_idx_update BEFORE INSERT OR UPDATE ON {TABLE}
        FOR EACH ROW EXECUTE PROCEDURE
        tsvector_update_trigger(search_field, 'pg_catalog.french', name)
        """
    )

    # FORMAT THE CITIES BEFORE INSERTING IN THE DATABASE
    cities_dict = [{"id": x.id, "name": x.name} for x in cities]
    cur.executemany(
        f"INSERT INTO {TABLE}(id,name) VALUES (%(id)s, %(name)s)", cities_dict
    )

    # SAVE THE INSERTS
    conn.commit()
    print("INSERT DONE")


if __name__ == "__main__":
    loaded_cities = load_file()
    init_db(loaded_cities)

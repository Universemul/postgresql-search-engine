from typing import List

import psycopg2


class PgService:
    DB_NAME = "test_search"
    DB_HOST = "localhost"
    DB_USER = "postgres"
    DB_PASSWORD = "postgres"

    def __init__(self):
        self.db = psycopg2.connect(
            f"dbname='{self.DB_NAME}' user='{self.DB_USER}' host='{self.DB_HOST}' password='{self.DB_PASSWORD}'"
        )

    def full_search_count(self, query: str) -> int:
        sql = (
            "SELECT count(*) FROM full_search WHERE search @@ to_tsquery('french', %s)"
        )
        cur = self.db.cursor()
        cur.execute(sql, (query,))
        return cur.fetchone()[0]

    def full_search(self, query: str) -> List:
        sql = (
            "SELECT id, name FROM full_search WHERE search @@ to_tsquery('french', %s)"
        )
        cur = self.db.cursor()
        cur.execute(sql, (query,))
        return [{"id": x[0], "name": x[1]} for x in cur.fetchall()]

    def full_search_highlight(self, query: str) -> List:
        sql = """
        WITH q AS (SELECT plainto_tsquery(%s) AS query),
        ranked AS (
            SELECT id, name, ts_rank(search, query) AS rank
            FROM full_search, q
            WHERE q.query @@ full_search.search
            ORDER BY rank DESC
        )
        SELECT id, ts_headline(name, q.query)
        FROM ranked, q
        ORDER BY ranked DESC
        """
        cur = self.db.cursor()
        cur.execute(sql, (query,))
        return [{"id": x[0], "highlight": x[1]} for x in cur.fetchall()]

    def get_cities(self, lat: float, lon: float, radius: int) -> List:
        cur = self.db.cursor()
        sql = """
            SELECT name, round(lat, 6), round(lon, 6)
            FROM full_search, (SELECT ST_MakePoint(%s, %s)::geography AS poi) AS f
            WHERE ST_DWithin(point, poi, %s);
        """
        cur.execute(
            sql,
            (
                lat,
                lon,
                radius,
            ),
        )
        return [
            {"name": x[0], "lat": float(x[1]), "lon": float(x[2])}
            for x in cur.fetchall()
        ]

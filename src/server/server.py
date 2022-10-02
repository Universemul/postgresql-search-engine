import json
import urllib.parse

import flask
import psycopg2

app = flask.Flask(__name__)

# Port on which JSON should be served up
PORT = 8001

# Database connection info
DB_NAME = "test_search"
DB_HOST = "localhost"
DB_USER = "postgres"
DB_PASSWORD = "postgres"

DB = psycopg2.connect(
    f"dbname='{DB_NAME}' user='{DB_USER}' host='{DB_HOST}' password='{DB_PASSWORD}'"
)


def _count(query: str):
    sql = """
        SELECT count(*)
        FROM full_search
        WHERE search_field @@ to_tsquery(%s)
    """
    cur = DB.cursor()
    cur.execute(sql, (query,))
    return cur.fetchone()[0]


def _do_full_text_search(query: str):
    sql = """
        SELECT id, name
        FROM full_search
        WHERE search_field @@ to_tsquery(%s)
    """
    cur = DB.cursor()
    cur.execute(sql, (query,))
    return [{"id": x[0], "name": x[1]} for x in cur.fetchall()]


def _do_highlights_full_text_search(query: str):
    sql = """
        WITH q AS (SELECT plainto_tsquery(%s) AS query),
        ranked AS (
            SELECT id, name, ts_rank(search_field, query) AS rank
            FROM full_search, q
            WHERE q.query @@ search_field
            ORDER BY rank DESC
        )
        SELECT id, ts_headline(name, q.query)
        FROM ranked, q
        ORDER BY ranked DESC
    """
    cur = DB.cursor()
    cur.execute(sql, (query,))
    return [{"id": x[0], "highlight": x[1]} for x in cur.fetchall()]


@app.route("/full_search/<query>")
def full_search(query: str) -> flask.Response:
    query = urllib.parse.unquote(query)
    count = _count(query)
    results = _do_full_text_search(query)
    ranked_results = _do_highlights_full_text_search(query)
    response = json.dumps(
        {
            "results": results,
            "ranked_results": ranked_results,
            "meta": {"count": count, "query": query},
        }
    )
    return flask.Response(response=response, content_type="application/json")


if __name__ == "__main__":
    app.debug = True
    app.run(port=PORT)

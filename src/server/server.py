import json
import urllib.parse
from typing import List

import flask
from flask import render_template

from src.server.pg_service import PgService

app = flask.Flask(
    __name__, template_folder="../client/templates", static_folder="../client/static"
)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Port of the app
PORT = 8001

service = PgService()


def _count(query: str) -> int:
    return service.full_search_count(query)


def _do_full_text_search(query: str) -> List:
    return service.full_search(query)


def _do_highlights_full_text_search(query: str) -> List:
    return service.full_search_highlight(query)


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


@app.route("/")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.debug = True
    app.run(port=PORT)

from flask import Flask, render_template, request
from index import search_word

webapp = Flask(__name__)


@webapp.route("/")
def landing_page():
    return render_template("lp.html")


@webapp.route("/search")
def search():
    srch = request.args.get("searchBox")
    limit = request.args.get("numberBox")
    res = []
    if srch:
        res = search_word(srch, limit)
    return render_template("search.html", res=res)

if __name__ == "__main__":
    webapp.run(debug=True)
from flask import Flask, render_template, request
from index import search_word

webapp = Flask(__name__)


@webapp.route("/")
def landing_page():
    return render_template("lp.html")


@webapp.route("/search")
def search():
    srch = request.args.get("searchBox")
    res = search_word(srch)
    return render_template("search.html", res=srch)

if __name__ == "__main__":
    webapp.run(debug=True)
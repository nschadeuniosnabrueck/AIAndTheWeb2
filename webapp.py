from flask import Flask, render_templates

webapp = Flask(__name__)


@webapp.route("/")
def landing_page():
    return render_templates("lp.html")



if __name__ == "__main__":
    webapp.run(debug=True)

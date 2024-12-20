from flask import Flask

webapp = Flask(__name__)


@webapp.route("/")
def landing_page():
    return """""
        <form action="URL to send the information" method="GET or POST">
            <input type="text" name="param">
            <input type="submit">
        </form>
          """

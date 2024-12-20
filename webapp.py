from flask import Flask

webapp = Flask(__name__)


@webapp.route("/")
def landing_page():
    return """""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Search Page</title>
    </head>
    <body>
        <h1>Search Something</h1>
        <input type="search" placeholder="Type here to search">
    </body>
    </html>
    """

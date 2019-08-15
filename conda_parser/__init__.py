from flask import Flask, request

from .parse import parse_environment


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return "OK"

    @app.route("/parse", methods=["POST"])
    def parse():
        """
            Page for posting a file to to get the Conda dependencies back.
            Solves a conda environment

            POST Parameters:
                file: an environment.y(a)ml file
            Returns:
                json with "error" or with "dependencies"/"channels"
        """
        return parse_environment(request.files.get("file"))

    return app


def main(debug=False):
    app = create_app()
    app.run(host="0.0.0.0", debug=debug)

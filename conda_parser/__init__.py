from flask import Flask, request

from .parse import parse_file


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return "OK"

    @app.route("/parse", methods=["POST"])
    def parse():
        """ Always make `/parse` go to latest version """
        return parse_v10()

    @app.route("/parse/v1.0", methods=["POST"])
    def parse_v10():
        """
            Page for posting a file to to get the Conda dependencies back.
            Tests just by looking at file as as string, not calling conda.
    
            POST Parameters:
                file: an environment.y(a)ml file
            Returns: 
                json with "error" or with "dependencies"/"channels"
        """
        return parse_file(request.files.get("file"))

    return app


def main(debug=False):
    app = create_app()
    app.run(host="0.0.0.0", debug=debug)

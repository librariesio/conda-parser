from flask import Flask, request

from .parse import parse_environment
from .info import package_info


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return "OK"

    @app.route("/info/<channel>/<package>/<version>")
    @app.route("/info/<channel>/<package>", defaults={"version": ""})
    @app.route("/info/<package>", defaults={"version": "", "channel": "anaconda"})
    def info(channel, package, version):
        return package_info(channel, package, version)

    @app.route("/parse", methods=["POST"])
    def parse():
        """
            Page for posting a file to to get the Conda dependencies back.
            Solves a conda environment

            POST Parameters two options:
                multipart/form-data:
                    file: an environment.y(a)ml file
                application/x-www-form-urlencoded:
                    file: the text of the environment file
                    filename: the filename (needs to be .yml or .yaml)
            Returns:
                json with "error" or with "dependencies"/"channels"
        """
        # get the file from either files or form
        if request.content_type.startswith("application/x-www-form-urlencoded"):
            body = request.form.get("file")
            filename = request.form.get("filename")
        elif request.content_type.startswith("multipart/form-data"):
            f = request.files.get("file")
            filename = f.filename if hasattr(f, "filename") else f.name
            body = f.read()

        return parse_environment(filename, body)

    return app


def main(debug=False):
    app = create_app()
    app.run(host="0.0.0.0", debug=debug)

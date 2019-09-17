from flask import Flask, request, jsonify, abort

from .parse import parse_environment
from .info import package_info

from conda.exceptions import ResolvePackageNotFound


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return "OK"

    @app.route("/info")
    def info():
        channel = request.args.get("channel", "pkgs/main")
        package = request.args.get("package", request.args.get("name"))  # Support package, or name being key
        version = request.args.get("version", "")
        return jsonify(package_info(channel, package, version)), 200

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

        return jsonify(parse_environment(filename, body)), 200

    @app.errorhandler(ResolvePackageNotFound)
    def not_found(e):
        message = f"Error: Package(s) not found: {e}"
        return jsonify(error=404, text=message), 404

    return app


def main(debug=False):
    app = create_app()
    app.run(host="0.0.0.0", debug=debug)

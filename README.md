# Conda parser

A tiny python web service for parsing dependency information from `environment.yml` files for [Libraries.io](https://libraries.io).

## Building and running options.

### Docker

You can use Docker to run conda-parser

First, install Docker. If you run macOS or Windows, Docker for Mac/Windows makes this really easy. (If you have Windows Home Edition, you'll need to download and run Docker Toolbox.)

Then, run:

    $ docker pull librariesio/conda-parser
    $ docker run -it -e PORT=5000 -p 5000:5000 librariesio/conda-parser

conda-parser will be running on http://localhost:5000.

To build the docker image locally:

    $ docker build -t librariesio/conda-parser .

Note: The Dockerfile has `./gunicorn_start.sh` as it's CMD so this can be overridden with `/bin/bash` if you'd like to poke around:

    $ docker run -it librariesio/conda-parser /bin/bash

### Docker Compose

Docker Compose makes this a lot easier, but there's one minor setup if using Docker for MacOS.
You must add the directory your cloned this to in the Docker Desktop -> Preferences -> File Sharing -> [+]  and Add the directory.

Then you can run

    $ docker-compose build
    $ docker-compose up

The server will be running, and any time you want to make a change to the code, you can just quit the `docker-compose up` process and re-run it. The new code will be reloaded. Because the `Dockerfile` and `gunicorn_start.sh` run Gunicorn, it won't auto reload when files are changed.

## Consuming the API

You can test that it works by running one of these curl commands:

```console
$ curl -X POST -F "file=@environment.yml" http://localhost:5000/parse # Post multipart

$ curl -X POST -F "file=<environment.yml;filename=environment.yml" http://localhost:5000/parse # Post urlencoded
```

To POST from something not curl (for example ruby `typhoeus`) please post a body with a file and a filename as such:

```ruby
# Post urlencoded
Typhoeus.post("http://localhost:5000/parse", body: {file: file_string, filename: 'environment.yml'})

# post multipart
Typhoeus.post("http://localhost:5000/parse", body: {file: File.open(filename, "r")})
```

(Both `multipart/form-data` and `application/x-www-form-urlencoded` are supported)

## Development

Most of the logic is in [conda_parser/parse.py](conda_parser/parse.py), the rest of the files are Flask/Tests/Gunicorn support. This file is a good place to start looking at the code.

Source hosted at [GitHub](http://github.com/librariesio/conda-parser).
Report issues/feature requests on [GitHub Issues](http://github.com/librariesio/conda-parser/issues). Follow us on Twitter [@librariesio](https://twitter.com/librariesio). We also hangout on [Slack](http://slack.libraries.io).

To get started, install [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) or Miniconda, and then run:

    $ conda env create -f environment.yml
    $ conda activate conda-parser

This will create you a conda-parser environment with all the packages installed from conda, (if you wish to not use conda for some reason, a requirements.txt file is also provided to `pip install`). To run the code, run either of the following lines:

    $ python flask_start.py
    $ FLASK_APP=conda_parser flask run

### Testing

This application uses `pytest` and `coverage.py`, to run tests, activate the conda environment and run one of the following lines:

    $ pytest
    $ pytest --cov=conda_parser
    $ pytest --cov=conda_parser --cov-report html  # To get a pretty html report


### Code Style

We use `black` for formatting.

    $ black .

### Note on Patches/Pull Requests

 * Fork the project.
 * Make your feature addition or bug fix.
 * Add tests if adding code.
 * Add documentation if necessary.
 * Make sure you run `black .` before submitting a pull request.
 * Send a pull request. Bonus points for topic branches.

## Copyright

Copyright (c) 2019 Tidelift. See [LICENSE](https://github.com/librariesio/conda-parser/blob/master/LICENSE) for details.

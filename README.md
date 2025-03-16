# Marsupial Gurgle Audio Archive Search Engine

## Overview

Flask-based web application that allows users to search the audio clips that have been uploaded to [Marsupial Gurgle](https://marsupialgurgle.com/).

## Requirements

- Node.js v22 LTS or newer
- Python 3.10 or newer
- MySQL Server 8.4 or newer

## Installation

Refer to [INSTALLING.md](./INSTALLING.md) for information on how to set up an instance of this web application that can be served through NGINX and Gunicorn.

## Changelog

For a list of changes between release versions of the application, refer to the included [CHANGELOG.md](./CHANGELOG.md).

## Contributing

If you would like contribute to this project, please make sure to review both the [Code of Conduct](./CODE_OF_CONDUCT.md) and the [Contributing](./CONTRIBUTING.md) documents in this repository.

## Licenses and Acknowledgements

This web application is licensed under the terms of the [MIT License](./LICENSE).

Additional packages that are distributed with the web application or reference available APIs
from libraries are distributed under the corresponding license terms listed below:

### Web Application Backend

- Flask
  - [3-Clause BSD License](https://github.com/pallets/flask/blob/main/LICENSE.txt)
- flask-sanitize-escape
  - [MIT License](https://github.com/mayur19/flask-sanitize-escape/blob/main/LICENSE)
- Gunicorn
  - [MIT License](https://github.com/benoitc/gunicorn/blob/master/LICENSE)
- MySQL Connector/Python
  - [GNU General Public License v2](https://downloads.mysql.com/docs/licenses/connector-python-9.2-gpl-en.pdf)
- python-slugify
  - [MIT License](https://github.com/un33k/python-slugify/blob/master/LICENSE)
- pytz
  - [MIT License](https://pythonhosted.org/pytz/#license)

### Web Application Frontend

- Bootstrap
  - [MIT License](https://github.com/twbs/bootstrap/blob/main/LICENSE)
- Bootstrap Color Mode Toggler
  - [Creative Commons Attribution 3.0 Unported](https://creativecommons.org/licenses/by/3.0/)
- Bootstrap Icons
  - [MIT License](https://github.com/twbs/icons/blob/main/LICENSE)
- IBM Plex Mono and Sans
  - [SIL Open Font License 1.1](https://github.com/IBM/plex/blob/master/LICENSE.txt)

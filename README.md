# Marsupial Gurgle Audio Archive Search Engine

## Overview

Flask-based web application that allows users to search the audio clips that have been uploaded to [Marsupial Gurgle](https://marsupialgurgle.com/).

## Requirements

- Node.js v22 LTS or newer
- Python 3.12 or newer
- MySQL Server 8.4 or newer

## Installation

Refer to [INSTALLING.md](./INSTALLING.md) for information on how to set up an instance of this web application that can be served through NGINX and Gunicorn.

## Changes

For a list of changes between release versions of the application, refer to the included [CHANGELOG.md](./CHANGELOG.md).

## Contributing

If you would like contribute to this project, please make sure to review both the [Code of Conduct](./CODE_OF_CONDUCT.md) and the [Contributing](./CONTRIBUTING.md) documents in this repository.

### AI Generated Code

Please note that this project does not accept pull requests or bugfixes that include code that has been partially or wholly generated using AI.

## Licenses and Acknowledgements

This web application is licensed under the terms of the [MIT License](./LICENSE).

Although this project interfaces with [MySQL Connector/Python](https://github.com/mysql/mysql-connector-python), licensed under version 2 of the GNU General Public License (GPLv2) and is also subject to the terms included in [Universal FOSS Exception, version 1.0](https://oss.oracle.com/licenses/universal-foss-exception/). The exception permits this library to be licensed under an OSI-approved or a license categorized as "free" by the Freedom Software Foundation (FSF), such as the MIT License.

[Bootstrap](https://github.com/twbs/bootstrap) and [Bootstrap Icons](https://github.com/twbs/icons) are both licensed under the terms of the [MIT License](https://github.com/twbs/bootstrap/blob/main/LICENSE).

[IBM Plex](https://github.com/IBM/plex/) is licensed under the terms of the [SIL Open Font License Version 1.1](https://github.com/IBM/plex/blob/master/LICENSE.txt).

Additional packages that are distributed with the web application or reference available APIs
from libraries are distributed under the corresponding license terms listed below:

### Web Application Backend

- Flask
  - [3-Clause BSD License](https://github.com/pallets/flask/blob/main/LICENSE.txt)
- flask-sanitize-escape
  - [MIT License](https://github.com/mayur19/flask-sanitize-escape/blob/main/LICENSE)
- Gunicorn
  - [MIT License](https://github.com/benoitc/gunicorn/blob/master/LICENSE)
- python-slugify
  - [MIT License](https://github.com/un33k/python-slugify/blob/master/LICENSE)
- pytz
  - [MIT License](https://pythonhosted.org/pytz/#license)

### Web Application Frontend

- Bootstrap Color Mode Toggler
  - [Creative Commons Attribution 3.0 Unported](https://creativecommons.org/licenses/by/3.0/)

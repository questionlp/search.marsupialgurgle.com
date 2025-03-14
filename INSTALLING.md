# INSTALLING

The following instructions target Debian 12 but also apply to other Linux distribution with `systemd`. The instructions assume that Python 3.10 (or newer) and the [pip](https://pip.pypa.io/en/stable/) tool are both installed and working.

This document provides instructions on how to serve the application through [Gunicorn](https://gunicorn.org) and use [NGINX](https://nginx.org/) as a front-end HTTP server. Other options are available for serving up applications built using Flask, but those options will not be covered here.

## Installing the Application

Clone a copy of this repository to a location of your choosing by running:

```bash
git clone https://github.com/questionlp/search.marsupialgurgle.com.git
```

Within the new local copy of the repository, create a new virtual environment and install the required packages by running the following commands:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

Next, make a copy of the `app_settings.json.dist` file with the name `app_settings.json` and a copy of the `database_settings.json.dist` file with the name `database_settings.json`. Edit both files and fill in the required application settings and database connection information.

To validate the installation, start up `gunicorn` using the following command while in the application root directory and with the virtual environment activated:

```bash
gunicorn search:app --reload
```

Once started, open a browser and browse to <http://127.0.0.1:8000/>. This should bring up the Reports web application.

## Building and Updating Bootstrap Theme

The Reports Site uses the Bootstrap frontend toolkit and a customized theme set that is referenced by the `scss` submodule. There should already be the necessary compiled CSS files stored under `app/static/css` as `app.css` and `app.min.css`.

In order to compile new versions of the CSS files, you will need to have the latest LTS version of Node.js installed. To install the necessary dependencies, run:

```bash
npm install
```

Once all of the dependencies are installed, you compile the appropriate CSS files and copy over the required JavaScript and font files into `app/static`.

```bash
npm run compile; npm run compile-minified
npm run copy-fonts; npm run copy-bundle; npm run copy-icons
```

## Configuring Gunicorn

Gunicorn can take configuration options either as command line arguments or it can load configuration options from a `gunicorn.conf.py` file located in the same directory that Gunicorn is launched from.

A template configuration file is included in the repository called `gunicorn.conf.py.dist`. A copy of that file should be made and named `gunicorn.conf.py` and the configuration options reviewed. The following options may need to be changed depending on the environment in which the application is being deployed:

* `bind`: The template defaults to using a UNIX socket file at
`/tmp/gunicorn-search-mg.sock` as the listener. If TCP socket is preferred, change the value to `IP:PORT` (replacing `IP` and `PORT` with the appropriate IP address of the interface and TCP port to listen to)
* `workers`: The number of processes that are created to handle requests.
* `accesslog`: The file that will be used to write access log entries to. Change the value from a string to `None` to disable access logging if that'll be handled by NGINX or a front-end HTTP server.
* `errorlog`: The file that will be used to write error log entries to. Change the value from a string to `None` to disable error logging (not recommended). The directory needs to be created before running the application.

For more information on the above configuration options and other configuration options available, check out the [Gunicorn documentation site](https://docs.gunicorn.org/en/stable/settings.html).

## Setting up a Gunicorn systemd Service

A template `systemd` service file is included in the repository named `gunicorn-mgsearch.service.dist`. That service file provides the commands and arguments used to start a Gunicorn instance to serve up the application. A copy of that template file can be modified and installed under `/etc/systemd/system`.

For this document, the service file will be installed as `gunicorn-mgsearch.service` and the service name will be `gunicorn-mgsearch`. The service file name, thus the service name, can be changed to meet your needs and requirements.

You will need to modify the following items in the new service file:

* `User`: The user which the service will run under
* `Group`: The group which the service will run under
* `WorkingDirectory`: Provide the full path to the application root directory. **Do not** include the `app` directory in the path
* `Environment`: Add the full path to the `venv/bin` directory
* `ExecStart`: Include the full path to the `venv/bin` directory and insert that between `ExecStart=` and `gunicorn`

Save the file and run the following commands to enable and start the new service:

```bash
sudo systemctl enable gunicorn-mgsearch
sudo systemctl start gunicorn-mgsearch
```

Verify that the service started by running the following command:

```bash
sudo systemctl status gunicorn-mgsearch
```

## Serving the Application Through NGINX

Once the service is up and running, NGINX can be configured to proxy requests to Gunicorn. NGINX can also be set up to cache responses and provide additional access controls that may not be feasible with Gunicorn.

Add the following NGINX configuration snippet either to your base `nginx.conf` or to a virtual site configuration file. The configuration settings provides a starting point for serving up the application.

```nginx
upstream gunicorn-mgsearch {
    server unix:/tmp/gunicorn-mgsearch.sock fail_timeout=0;
}

server {
    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_pass http://gunicorn-mgsearch;
    }
}
```

NGINX can also be configured to cache rendered pages to quickly serve up pages that are commonly and frequently requested. NGINX has documentation on configuring and enable proxy caching in their [ngx_http_proxy_module](https://nginx.org/en/docs/http/ngx_http_proxy_module.html) module documentation.

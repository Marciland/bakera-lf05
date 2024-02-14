# Feinstaubstation

This project is created for school. Therefore we (the [contributors](#contributors)) do not guarantee any kind of maintenance after finishing the project in school, nor do we guarantee that the project is running as expected.

As per specifications in school this project can:

- crawl data from [Luftdaten](https://luftdaten.info/)
- feed the data into a database
- provide an API to get certain data
- as per specification "certain" means:
  - min/max/average temperature for the 14.03.2022
  - per date and type(temperature/humidity/particulate matter): min/max/average

### Optional GUI

If we are fast enough with planning and development, we might provide a GUI (Graphical User Interface) aside from the automatically generated API documentation

## Requirements

This project is based on docker to reduce dependencies and ease the development as well as the testing process.

Thus it is required to be able to run docker in order to execute this application (API & DB).

On Windows this can either be achieved by installing [Docker Desktop](https://www.docker.com/products/docker-desktop/) or by setting up docker in a [WSL](https://www.paulsblog.dev/how-to-install-docker-without-docker-desktop-on-windows/).

Either of these require virtualization (any hypervisor).

### Side note on docker

Some of us decided against Docker Desktop due to company policies.

## How to run

> optionally: a network will allow us to reach the database using its container name instead of an IP

`docker network create NETWORK`

Create a volume for postgres to persist the data inside our database (e.g. tables)!

`docker volume create VOLUMENAME`

This command will run a database container:

> Specify NAME, VOLUMENAME when doing so!
> POSTGRES_USER, POSTGRES_PASSWORD are referenced in main.py and therefore static.

`docker run -d --name NAME -p 5432:5432 --restart always --network NETWORK -v VOLUMENAME:/var/lib/postgresql/data -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=password postgres:15.3-bullseye`

We are going to use psycopg3 (psycopg) in python, thus we are working with postgres version 15 (currently the highest supported version for psycopg3).

#

Optionally run a pgadmin container to have a GUI when working with the database. Do not use the same volume as the database volume!

> PGADMIN_LISTEN_PORT should be the same as the containers port specified in dockers -p parameter. Host port does not matter and can be freely chosen.

`docker run -d --name NAME -p PORT:PGADMIN_LISTEN_PORT --restart always --network NETWORK -v VOLUMENAME:/var/lib/pgadmin -e PGADMIN_DEFAULT_EMAIL=MAIL@MAIL.MAIL -e PGADMIN_DEFAULT_PASSWORD=PASS -e PGADMIN_LISTEN_ADDRESS=0.0.0.0 -e PGADMIN_LISTEN_PORT=PORT dpage/pgadmin4:8.3`

#

Running the API requires to build an image on which we run on:

> The context from which docker is started matters! Run this command from within the root directory of this project (where the Dockefile is present)

`docker build --pull --no-cache --force-rm --tag IMAGENAME:IMAGETAG .`

After successfully building the API image you can run a container based on the image using this command:

`docker run -d --name NAME -p PORT:PORT --restart always --network NETWORK IMAGENAME:IMAGETAG`

## Contributors

<a href="https://github.com/Marciland">Marciland</a><br/>
<a href="https://github.com/Speedl1ng">Speedl1ng</a><br/>
<a href="https://github.com/Nostr0">Nostr0</a><br/>
<a href="https://github.com/AlinaFlick">AlinaFlick</a>

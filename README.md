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

Specify NAME, USER, PASS when running the following command:

`docker run -d --name NAME -p 5432:5432 -v /var/lib/postgresql/data:/var/lib/postgresql/data -e POSTGRES_USER=USER -e POSTGRES_PASSWORD=PASS postgres:15.3-bullseye`

We are going to use psycopg3 (psycopg) in python, thus we are working with postgres version 15 (currently the highest supported version for psycopg3).

Optionally run a pgadmin container to have a GUI when working with the database.

`docker run -d --name NAME -v /var/lib/pgadmin:/var/lib/pgadmin -e PGADMIN_DEFAULT_EMAIL=EMAIL -e PGADMIN_DEFAULT_PASSWORD=PASS -e PGADMIN_LISTEN_ADDRESS=IP -e PGADMIN_LISTEN_PORT=PORT IMAGENAME:IMAGETAG`

`docker build --pull -no-cache --force-rm --tag IMAGETAG .`

`docker run -d --name NAME -p PORT:PORT IMAGENAME:IMAGETAG`

## Contributors

<a href="https://github.com/Marciland">Marciland</a><br/>
<a href="https://github.com/Speedl1ng">Speedl1ng</a><br/>
<a href="https://github.com/Nostr0">Nostr0</a><br/>
<a href="https://github.com/AlinaFlick">AlinaFlick</a>

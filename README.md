# visitor-signin

## Prerequisites
### Common
 - A copy of sqlite database in:
   - `./production/database`

### Normal System
 - Install [Docker](https://docs.docker.com/install/)
 - Install [Docker-Compose](https://docs.docker.com/compose/install/#prerequisites)

### Raspberry Pi
Note: Only tested on Raspbian
 - Install Docker
 `curl -sSL https://get.docker.com | sh`
 - Install Docker-Compose:
 ```
 sudo apt-get install python-pip
 sudo pip install docker-compose
 ```

## Deployment
Clone repo and ensure both build and run scripts are executable:
 ```
 git clone https://github.com/kamsandhu93/visitor-signin.git
 cd visitor-signin
 chmod +x ./run.sh
 chmod +x ./build.sh
 ```

 To build images:
 ```
 ./build.sh [OPTIONAL_COMMANDS]
 <enter root password as docker needs to run as root>
 ```

 To run containers:
 ```
 ./run.sh [OPTIONAL_COMMANDS]
 <enter root password as docker needs to run as root>
 ```

### Optional commands
#### build.sh
```
-h
    show help
-s [CONTAINER_NAME_IN_COMPOSE]
    Allow a single selected container to be built. Without this option all containers are built
```

#### run.sh
```
-h
    Show help
-d
    Start all containers in debug mode
-r
    Force recreate all containers even when there are no changes
-H
    Host IP address the frontend will send request to (default: 127.0.0.1)
-b
    Directory of database offline backup (default: /opt/visitorsignin/offline_backup)
-f
    Name of database file (default: visitor_db.db)
```

After deployment has finished
frontend will be available at: `http://localhost:5003`
database admin panel will be available at: `http://localhost:5001`

## System Infrastructure
The system is made up of five docker containers

### frontend
 - Progressive web application served by node http-server
 - Communicates with both `print` and `database-api` containers

### database-api
 - Hosts the flask app that serves the api for sign in and sign out
 - Communicates with backup service

### database-admin
 - Hosts the database admin website

### print
 - Hosts print service

Production file structure on the host system:
```
./production
|
└─── database
|   └─── visitor_db.db
└─── log
    |
    └─── database_api.log
    └─── print.log
```
The database file `visitor_db.db` is persisted to all three containers.

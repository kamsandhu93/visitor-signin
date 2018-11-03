# visitor-signin

## Prerequisites
### Common
 - curl
 - A [Dropbox](https://www.dropbox.com) account
 - Created a dropbox app and generated a dropbox api token in [Dropbox Developer Console](https://www.dropbox.com/developers/apps)
 - A copy of sqlite database in either:
   - `/opt/visitorsigin/database` or
   - Dropbox app root folder - e.g. if your app is called VisitorSignin, the database file should be in `Dropbox/Apps/VisitorSignin`
### Normal System
 - Install [Docker](https://docs.docker.com/install/)
 - Install [Docker-Compose](https://docs.docker.com/compose/install/#prerequisites)
### Raspberry Pi
Note: Only tested on Raspbian
 - Install Docker
 `curl -sSL https://get.docker.com | sh`
 - Install Docker-Compose:
 ```
 sudo apt-get install python pip
 sudo pip install docker-compose
 ```

## Deployment
 ```
 git clone https://github.com/kamsandhu93/visitor-signin.git
 cd visitor-signin
 chmod +x ./deploy.sh
 ./deploy.sh -t [DROPBOX_TOKEN] [OPTIONAL_COMMANDS]
 <enter root password as docker needs to run as root>
 ```

### Optional commands
```
-h
    Show help
-H
    Host IP address the frontend will send request to (default is the first 192. IP address of ifconfig)
-d
    Start all containers in debug mode
-b
    Force rebuild of all images and recreate all containers even when there are no changes
-r
    Force recreate all containers even when there are no changes
-f
    Name of database file (default: visitor_db.db)
-c [CONTAINER_NAME_IN_COMPOSE]
    Allow a single selected container to be started. The -b option will overwrite this option
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

### database-admin
 - Hosts the database admin website

### print
 - Hosts print service

### backup
 - Hosts the backup and restore scripts
 - Database is checked every 30 seconds for changes and is backed up if there are changes
To perform a forced restore, run:
```
sudo docker ps
<copy the container id of the backup container>
sudo docker exec -it <container id> /bin/sh
cd /backupservice
python database_operations.py -o "restore_force"
```

During deployment `deploy.sh` creates the following file structure on the host system:
```
/opt/visitorsignin
|
└─── database
|   └─── visitor_db.db
└─── log
    |
    └─── database_api.log
    └─── backup.log
    └─── print.log
```
The database file `visitor_db.db` is persisted to all three containers.

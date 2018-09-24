# visitor-signin

## Prerequisites
 - Install [Docker](https://docs.docker.com/install/)
 - Install [Docker-Compose](https://docs.docker.com/compose/install/#prerequisites)
 - A [Dropbox](https://www.dropbox.com) account
 - Created a dropbox app and generated a dropbox api token in [Dropbox Developer Console](https://www.dropbox.com/developers/apps)
 - A copy of sqlite database in either:
   - `/opt/visitor-db/database` or
   - Dropbox app root folder - e.g. if your app is called VisitorSignin, the database file should be in `Dropbox/Apps/VisitorSignin`

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
-d, --debug
    Start both containers in debug mode
-b, --build
    Force rebuild of both containers even when there are no changes
-db, --database
    Name of database file (default: visitor_db.db)
-br, --branch
    Select which branch to use (default: master)
```

After deployment has finished
visitor app will be available at: `http://localhost:5000`
sqlite database control panel will be available at: `http://localhost:5001`

## System Infrastructure
The system is made up of three docker containers with the sqlite database persisted between all three and the host.

### Visitor-Flask
 - Hosts the flask app that serves the front end of the visitor signin app.
 - Flask app writes to `/visitor-app/database/visitor_db.db` inside the container.

### Visitor-Database
 - Hosts the database control panel web app for the sqlite database.
 - Reads and writes to `/visitor-db/database/visitor_db.db` inside the container.

### Visitor-Back
 - Hosts the backup and restore scripts.
 - If there is no database detected, the script will download a copy of the database from dropbox during deployment.
 - Database is backedup to dropbox every day at 01:00 server time.
 - Reads and writes to `/visitor-back/database/visitor_db.db` inside the container.
To perform a forced restore, run:
```
sudo docker ps
<copy the container id of the backup container>
sudo docker exec -it <container id> /bin/sh
cd /visitor-back
python db_ops.py -t <dropbox token> -p /visitor-back/database -l /visitor-back/log -f <database file name> -o "restore_force"
```

During deployment `deploy.sh` creates the following file structure on the host system:
```
/opt/visitor-db
|
└─── database
|   └─── visitor_db.db
└─── log
    |
    └─── flask
    |   └─── visitor.log
    └─── backup
        └─── backup.log
```
The database file `visitor_db.db` is persisted to all three containers.
`visitor.log` contains all logs from the flask app.
`backup.log` contains all logs from the backup and restore script.

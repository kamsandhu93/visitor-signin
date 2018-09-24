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

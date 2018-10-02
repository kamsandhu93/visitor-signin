# visitor-signin

## Prerequisites
N.B. Commands assuming Ubuntu
 - curl
    ```
    sudo apt-get install curl
    ```
 - Install [Node.js](https://nodejs.org/en/download/)
    ```
    sudo apt-get update
    sudo apt-get install nodejs
    sudo apt-get install npm
    ```
    Verify node and npm installed correctly, Node >=8 needed (till this moment)
    ```
    node -v # Expected Version 
    npm -v # Expected Version
    ```
    If you already have an old version of node, you will need to upgrade it
    ```
    sudo npm cache clean -f
    sudo npm install -g n
    sudo n stable  #if needed (sudo n latest)
        OR
    wget -qO- https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh | bash # install nvm (node version manager)
    nvm install stable
    ```
 - Install [Docker](https://docs.docker.com/install/)
    ```
    sudo apt-get update
    sudo apt-get install apt-transport-https ca-certificates software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    sudo apt-get update
    sudo apt install docker-ce
    ```
    Verify docker installed correctly
    ```
    sudo docker run hello-world
    ```
 - Install [Docker-Compose](https://docs.docker.com/compose/install/)
    
    ```
    # find out what is the latest release from https://github.com/docker/compose/releases/ 
    # then replace the release number in the url with the version you want to install
    sudo curl -L "https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    ```
    Verify
    ```
    docker-compose --version
    ```
 - A [Dropbox](https://www.dropbox.com) account
 - Create a Dropbox API app [Dropbox Developer Console](https://www.dropbox.com/developers/apps)
    - Choose app folder
    - Name: must be globaly unique choose any name and take a note of it
    - After creating the app, click `Generate access token`
 - A copy of sqlite database in either:
   - (Locally) `/opt/visitor-db/database/` or
   - (on Dropbox) Dropbox app root folder - e.g. if your app is called VisitorSignin, the database file should be in `Dropbox/Apps/VisitorSignin`
   - if you dont have a copy and this a fresh deployment create an empty database file locally, default name for the file is `visitor_db.db`

Alternatively run the following script


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
-d
    Start all containers in debug mode
-b
    Force rebuild of all images and recreate all containers even when there are no changes
-r
    Force recreate all containers even when there are no changes
-f
    Name of database file (default: visitor_db.db)
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
 - Database is backedup to dropbox every day at 01:00 server time.
 - Reads and writes to `/visitor-back/database/visitor_db.db` inside the container.
To perform a forced restore, run:
```
sudo docker ps
<copy the container id of the backup container>
sudo docker exec -it <container id> /bin/sh
cd /visitor-back
python db_ops.py -o "restore_force"
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

# visitor-signin

## Local deployment
The flask_app directory needs to be marked as sources root

A copy of the sqllite databse needs to be placed in the flask_app/instance directory


## Prerequisites
 - Install [Docker](https://docs.docker.com/install/)
 - Install [Docker-Compose](https://docs.docker.com/compose/install/#prerequisites)

## Deployment
 ```
 git clone https://github.com/kamsandhu93/visitor-signin.git
 cd visitor-signin
 chmod +x ./deploy.sh
 ./deploy.sh [OPTIONAL_COMMANDS]
 ```

### Optional commands
```
-d, --debug
    Start both containers in debug mode
-b, --build
    Force rebuild of both containers even when there are no changes
```

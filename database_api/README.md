# visitor-signup database-api
API for managing visitor sign in and sign out

## Project Dependencies
### Main Dependencies
 - Python 3
 - pip

### Packages
 - [flask](http://flask.pocoo.org/)
 - [flask-cors](https://github.com/corydolphin/flask-cors)
 - [requests](https://github.com/requests/requests)

## Infrastructure
### Endpoints
 - `/login` - POST
   - Receives the following data structure:
   ```
   {
       "name": <string>,
       "surname": <string>,
       "visiting": <string>,
       "company": <string>
   }
   ```
   - Generates a unique pass ID
   - Writes the received data along with pass ID and signin time to database
   - Sends request to backup services to backup data
   - Returns pass ID to the request sender
 - `/logout` - POST
   - Receives the following data structure:
   ```
   {
       "passId": <string>
   }
   ```
   - Finds the corresponding entry in the database and appends signout time
   - Sends request to backup services to backup data
   - Returns first and last names to the request sender

### Database
Database location is `/home/database`. This is persisted to `./production/database` of the repository on host

### Logging
Log location is `/home/log`. This is persisted to `./production/log` of the repository host

### Configuration
The flask application can be configured by setting environmental variables before running.
 - HOST - Host of flask application (default: 127.0.0.1)
 - PORT - Port of flask application (default: 5000)
 - LOG_PATH - Absolute path of log file (e.g. /home/log/database_api.log)
 - DB_PATH - Absolute path of database file (e.g. /home/database/visitor_db.db)
 - REQUEST_HOST - Host IP of backup service (default: 127.0.0.1) - The host is automatically set by `start.sh` to the bridge IP when running in a container.

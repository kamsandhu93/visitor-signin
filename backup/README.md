# visitor-signup backup

## Project Dependencies
### Main Dependencies
 - Python 3
 - pip

### Packages
 - [flask](http://flask.pocoo.org/)
 - [flask-cors](https://github.com/corydolphin/flask-cors)
 - [dropbox](https://github.com/dropbox/dropbox-sdk-python)

## Infrastructure
### Endpoints
 - `/backup` - POST
   - Does not require a body
   - Triggers backup to both dropbox and local
 - `/restore` - POST
   - Receives the following data structure:
   ```
   {
       "forced": <boolean>
   }
   ```
   - Restore will overwrite existing database if forced flag is set to true
   - Restore will only occur if there is no existsing daabase if forced flag is set to false

### Database
Database location is `/backupservice/database`. This is persisted to `/opt/visitorsignin/database` of the host

### Logging
Log location is `/backupservice/log`. This is persisted to `/opt/visitorsignin/log` of the host

### Offline Backup
Offline backup location is `/backupservice/offline_backup`. This is persisted to OFFLINE_BACKUP_PATH of the host (default: `/opt/visitorsignin/offline_backup`)

### Configuration
The flask application can be configured by setting environmental variables before running.
 - HOST - Host of flask application (default: 127.0.0.1)
 - PORT - Port of flask application (default: 5004)
 - LOG_PATH - Absolute path of log file (e.g. /backupservice/log/backup.log)
 - DB_FILE - Database file name (default: visitor_db.db)
 - DB_PATH - Absolute path of database file directory (e.g. /backupservice/database)
 - DROPBOX_TOKEN - Dropbox API Token (please see main README for more information)

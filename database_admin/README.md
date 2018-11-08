# visitor-signin database-admin
Website to view and edit database data
## Project Dependencies
### Main Dependencies
 - Python 3
 - pip
### Packages
 - sqlite-web

## Infrastructure
Hosts [sqlite-web](https://github.com/coleifer/sqlite-web) package in the container.

### Database
Database file location is `/databaseadmin/database`. This is persisted to `/opt/visitorsignin/database` of the host.

### Logging
Log location is `/databaseadmin/log`. This is persisted to `/opt/visitorsignin/log` of the host

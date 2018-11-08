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
Database file location is `/databaseadmin/database`. This is mounted to `/opt/visitorsignin/database` of the host.

# visitor-signin database-admin
Website to view and edit database data
## Project Dependencies
### Main Dependencies
 - Python 3
 - pip
### Packages
 - [sqlite-web](https://github.com/coleifer/sqlite-web)

## Infrastructure
Hosts [sqlite-web](https://github.com/coleifer/sqlite-web) package in the container.

### Database
Database file location is `/home/database`. This is persisted to `./production/database` of the repository on host.

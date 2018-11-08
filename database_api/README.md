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
       "name": "firstname",
       "surname": "surname",
       "visiting": "visiting",
       "company": "A Company"
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
       passId: "00045a"
   }
   ```
   - Finds the corresponding entry in the database and appends signout time
   - Sends request to backup services to backup data
   - Returns first and last names to the request sender

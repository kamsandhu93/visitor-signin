# visitor-signin frontend
Frontend Progressive Web Application of visitor signin system
## Project Dependencies
 - [Node.js](https://nodejs.org/en/)

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Run tests
```
npm run test
```

### Hosting for production
```
npm install -g http-server
npm build
http-server dist -a <IP> -p <Port>
```

## Infrastructure
This is a Single Page Progressive Web Application created using [Vue.js](https://vuejs.org/). The base structure was generated using [Vue-cli](https://cli.vuejs.org/).

### Packages
##### [Vue Router](https://router.vuejs.org/)
 - Used for routing control of the web app
##### [Vuex](https://vuex.vuejs.org/)
 - Central store:
   - Service status
   - Printer and database api host/port
##### [nhsuk-frontend-vue](https://github.com/xLasercut/nhsuk-frontend-vue)
 - UI library
##### [vue-qrcode-reader](https://github.com/gruhn/vue-qrcode-reader)
 - QR code reader for web cam for sign out page
##### [qrcode.vue](https://github.com/scopewu/qrcode.vue)
 - QR code image generator for visitor pass example page
##### [axios](https://github.com/axios/axios)
 - Promise based request library for http requests
##### [cypress](https://docs.cypress.io/guides/overview/why-cypress.html#In-a-nutshell)
 - Test runner

## Workflow
```
                                User
                                  +
                                  v
                             +----+------+
                             | Home Page +<---------------------+
                             +--+----+---+                      |
                                |    |                          |
             +--------------+   |    |    +---------------+     |
             | Sign In Page +<--+    +--->+ Sign Out Page |     |
             +-----------+--+             +--+------------+     |
                         |                   |                  |
                         v                   v                  |
                      +--+-------------------+---+              |
              +-------+   POST to database api   |              |
      Sign In |       +-----+-------------------++              |
      Success |             |                   |               |
              v             |                   |               |
+-------------+------+      |                   |               |
| POST to Print Pass |      |                   |               |
+----------+--------++      |                   |               |
           |        |       |                   |               |
           |        | Error |          Sign out |               |
           |        v       v          Success  v               |
           |        +-------+----+   +----------+--------+      |
           |        | Error Page |   | Confirmation Page +------+
           |        +------------+   +----+--------------+
           |                              ^
           |                              |
           |        Print Success         |
           +------------------------------+

```

# Visitor Signin Frontend

> Front end of visitor signin system

## Prerequisites
 - Install [Node.js](https://nodejs.org/en/download/)

## Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:9080
npm run dev

# build electron application for production
npm run build


```

## Setting Request URL and Printer
If no `config.json` is found in the same directory as the application. A default is used:
```
host: localhost
port: 5000
printer: Microsoft Print to PDF
```
To change the default setup, create `config.json` in the same directory as the application with structure:
``` json
{
    "host": "<your host>",
    "port": "<your port>",
    "printer": "<printer name>"
}
```

---

This project was generated with [electron-vue](https://github.com/SimulatedGREG/electron-vue)@[88c386d](https://github.com/SimulatedGREG/electron-vue/tree/88c386d59c5f0b17046afc6adc7fa1170e85c6b8) using [vue-cli](https://github.com/vuejs/vue-cli). Documentation about the original structure can be found [here](https://simulatedgreg.gitbooks.io/electron-vue/content/index.html).

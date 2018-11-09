#/bin/bash

echo "const env = { REQUEST_HOST: '$REQUEST_HOST' }" > dist/env.js

http-server dist -a $HOST -p $PORT

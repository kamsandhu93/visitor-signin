#/bin/bash

response=$(curl --write-out %{http_code} --silent --output /dev/null http://$HOST:$PORT)

if [[ "$response" != "200" ]]; then
    exit 1
fi
exit 0

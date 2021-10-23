#!/bin/bash
set -e
cd $(dirname $0)
source common.sh

docker build --pull -t $image_name .

docker run --rm -it -p 9000:8080 \
  -e "DEVELOPER_MODE=true" \
  -e "LOG_LEVEL=INFO" \
  -e "FLASK_APP=main.py" \
  -e "FLASK_DEBUG=1" \
  -e "WERKZEUG_DEBUG_PIN=off" \
  -e "CLIENT_ID=clientid" \
  -e "CLIENT_SECRET=secret" \
  -e "ACCESS_TOKEN=token" \
  -e "TOKEN_ISSUED_DATE=2021-10-15 16:00:28.816581" \
  -e "TOKEN_EXPIRES_IN=1799" \
  $image_name:latest \
  app.handler

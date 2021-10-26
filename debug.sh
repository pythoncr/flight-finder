#!/bin/bash
set -e

docker build -t flight_finder_logger_python:local .

docker run --rm -it -p 9000:8080 \
  flight_finder_logger_python:local \
  app.handler

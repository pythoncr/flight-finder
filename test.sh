#!/bin/bash
set -e
cd $(dirname $0)
source common.sh

docker build --pull -t ${image_name} .

if [ -f test.env ]; then
    ENV_FILE="test.env"
fi

docker run \
  --rm ${ENV_FILE:+ --env-file ${ENV_FILE}} \
  -v $(pwd)/test:/test \
  -v $(pwd)/htmlcov/:/app/htmlcov \
  -v $(pwd)/output/:/output \
  ${image_name} \
  app.handler \
  pytest --cov-report html --cov-report xml:/output/coverage.xml --cov=/app --junitxml /output/results.xml /test "$@"

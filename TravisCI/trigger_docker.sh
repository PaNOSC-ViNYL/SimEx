# based on https://gist.github.com/domenic/ec8b0fc8ab45f39403dd

#!/bin/bash
set -e # Exit with nonzero exit code if anything fails

# check python version
if [ "$TRIGGER_DOCKER_FOR_PYTHON" != "$TRAVIS_PYTHON_VERSION" ]; then
    echo "Skipping trigger Docker for python " $TRAVIS_PYTHON_VERSION
    exit 0
fi

SOURCE_BRANCH="develop"

# Pull requests and commits to other branches shouldn't try to trigger
if [ "$TRAVIS_PULL_REQUEST" != "false" -o "$TRAVIS_BRANCH" != "$SOURCE_BRANCH" ]; then
    echo "Skipping trigger Docker"
    exit 0
fi

curl -H "Content-Type: application/json" --data '{"build": true}' -X POST https://registry.hub.docker.com/u/yakser/simex/trigger/3777241e-0a74-42ad-8382-d9b3c5f1465a/


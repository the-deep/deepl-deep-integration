#!/bin/bash

export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

# Name of docker image
DEEPL_IMG_NAME=deepl_extractor_entry_predictor

# Change if key is not in default location
# Make sure the public key is already loaded in your github account
SSH_PRIVATE_KEY_PATH=~/.ssh/id_rsa

export SSH_PRV_KEY=$SSH_PRIVATE_KEY_PATH

# If ssh-agent is not running, below command runs it
if [ $(ps ax | grep [s]sh-agent | wc -l) -gt 0 ] ; then
    echo "ssh-agent is already running"
else
    eval `ssh-agent -s`
fi

# Add the ssh key
ssh-add $SSH_PRIVATE_KEY_PATH

# If you want to build container with Dockerfile, execute below command
docker build --ssh default -t $DEEPL_IMG_NAME -f Dockerfile .

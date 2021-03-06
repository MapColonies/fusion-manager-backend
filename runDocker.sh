#!/bin/bash

# Default values of arguments
ENTERYPOINT=0

# Loop through arguments and process them
# Taken from: https://pretzelhands.com/posts/command-line-flags
for arg in "$@"
do
    case $arg in
        --entrypoint)
        ENTERYPOINT=1
        shift # Remove
        ;;
    esac
done

if [ $ENTERYPOINT -eq 1 ]; then
    docker run --rm -it --entrypoint /bin/bash -v /opt/google/share/tutorials/fusion:/opt/google/share/tutorials/fusion --name serversidecontainer -p 8081:8000 serverside:v1
else
    docker run --rm -v /opt/google/share/tutorials/fusion:/opt/google/share/tutorials/fusion --name serversidecontainer -p 8081:8000 serverside:v1 &
fi

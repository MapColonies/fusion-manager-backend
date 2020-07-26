#!/bin/bash

apt-get install -y $(grep -vE "^\s*#" apt-requirements.txt  | tr "\n" " ")

pip install -r "pip-requirements.txt"
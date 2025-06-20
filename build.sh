#!/bin/bash

# Download config.yaml
curl -L -o config.yaml "https://drive.google.com/file/d/1sRoqZrTNgLDJIbgEuvcNzIJZEjdL4Wei/view?usp=drive_link"

# Install Python packages
pip install -r requirements.txt
#!/bin/bash

# Download config.yaml from Google Drive
curl -L -o config.yaml "https://drive.google.com/uc?export=download&id=1sRoqZrTNgLDJIbgEuvcNzIJZEjdL4Wei"

# Install dependencies
pip install -r requirements.txt
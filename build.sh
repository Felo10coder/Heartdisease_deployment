#!/bin/bash

# Function to download Google Drive file using file ID
FILE_ID="1sRoqZrTNgLDJIbgEuvcNzIJZEjdL4Wei"
DESTINATION="config.yaml"

echo "Downloading config.yaml from Google Drive..."

wget --no-check-certificate "https://drive.google.com/uc?export=download&id=${FILE_ID}" -O ${DESTINATION}

# Install dependencies
pip install -r requirements.txt
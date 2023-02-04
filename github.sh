#!/bin/bash

# Run the Python script
python3 main.py

# Add all files in the out directory to the Git index
git add ./out

# Commit the changes with a message
git commit -m "Update data"

# Push the directory to GitHub
git push origin main

#!/bin/bash

# Bash-script to quickly get the pinned dependencies for a specific super-linter tag

# Define the TAG variable
TAG="v5" # Replace with the desired tag

# Create a temporary directory
TEMP_DIR=$(mktemp -d -p "$(pwd)")

# Clone the repository into the temporary directory
git clone https://github.com/super-linter/super-linter.git --branch $TAG $TEMP_DIR

# Check if the clone was successful
if [ $? -ne 0 ]; then
    echo "Failed to clone the repository."
    exit 1
fi

# Navigate to the dependencies/python directory
cd $TEMP_DIR/dependencies/python/

# Combine all .txt files into one
cat *.txt > superlinter_dependencies.txt

# Copy the superlinter_dependencies.txt to the original repository
cp superlinter_dependencies.txt /home/thijs/dev/cemsbv/github/py-pilecore/

# Navigate back to the original repository
cd -

# Remove the temporary directory
rm -rf $TEMP_DIR
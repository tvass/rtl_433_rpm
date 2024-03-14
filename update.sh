#!/bin/bash
# Script to update the git commit reference and trigger a new build at COPR.

# Configuration
RTL_433_DIR="../rtl_433/"
SPEC_FILE="rtl_433.spec"

cd "$RTL_433_DIR" || { echo "Error: Could not change directory to $RTL_433_DIR"; exit 1; }

# Get the latest commit hash
git pull
latest_commit_hash=$(git rev-parse HEAD) || { echo "Error: Failed to get the latest commit hash"; exit 1; }
echo "Latest commit hash: $latest_commit_hash"

# Return to the previous directory
cd - || { echo "Error: Could not change directory back"; exit 1; }

# Update the commit hash in the spec file
sed -r "3s/.*/%global         github_commit $latest_commit_hash/" "$SPEC_FILE" > tmpfile || { echo "Error: Failed to update commit hash in $SPEC_FILE"; exit 1; }
mv tmpfile "$SPEC_FILE" || { echo "Error: Failed to rename tmpfile to $SPEC_FILE"; exit 1; }

if ! git diff --exit-code "$SPEC_FILE" >/dev/null 2>&1; then
    git add "$SPEC_FILE" || { echo "Error: Failed to add $SPEC_FILE to the staging area"; exit 1; }
    git commit -m "Update commit to $latest_commit_hash" || { echo "Error: Failed to commit changes"; exit 1; }
    git push || { echo "Error: Failed to push changes to remote repository"; exit 1; }
    echo "Changes pushed to remote repository."
else
    echo "No changes in the repository."
fi

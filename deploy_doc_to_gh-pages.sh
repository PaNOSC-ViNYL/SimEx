#!/bin/bash
###
# Script to copy html doc from build dir to repository root and push to gh-pages for automatic page creation. Assumes built html sources reside in Sources/doc/build/html.
set -e # Exit with nonzero exit code if anything fails

# Set branch from which to deploy.
SOURCE_BRANCH="master"
TARGET_BRANCH="gh-pages"

# Pull requests and commits to other branches shouldn't try to deploy, just build to verify
if [ "$TRAVIS_PULL_REQUEST" != "false" -o "$TRAVIS_BRANCH" != "$SOURCE_BRANCH" ]; then
    echo "Skipping deploy; just doing a build."
    exit 0
fi

# Save some useful information
REPO=`git config remote.origin.url`
COMMIT_AUTHOR_EMAIL=`git config user.email`
SSH_REPO=${REPO/https:\/\/github.com\//git@github.com:}
SHA=`git rev-parse --verify HEAD`

# Save html content to a place not tracked by git.
cp -arv Sources/doc/build/html ._html

# Checkout target branch ( = gh-pages).
git checkout -b ${TARGET_BRANCH}

# Cleanup.
rm -rfv */
rm -v CMakeLists.txt
rm -v copyright_notice.py
rm -v deploy_doc_to_gh-pages.sh
rm -v install.exfl.sh
rm -v install.sh
rm -v README.md
rm -v requirements.txt
rm -v simex_dev.in
rm -v simex.in
rm -v simex_vars_dev.sh.in
rm -v simex_vars.sh.in

# Move html content to root.
mv -v ._html/* .

# Configure git.
git config user.name "Carsten Fortmann-Grote"
git config user.email "carsten.grote@xfel.eu"
# Commit.
git add --all
git commit -m "Installed gh-pages content for ${SHA}"

# Get the deploy key by using Travis's stored variables to decrypt deploy_key.enc
ENCRYPTED_KEY_VAR="encrypted_${ENCRYPTION_LABEL}_key"
ENCRYPTED_IV_VAR="encrypted_${ENCRYPTION_LABEL}_iv"
ENCRYPTED_KEY=${!ENCRYPTED_KEY_VAR}
ENCRYPTED_IV=${!ENCRYPTED_IV_VAR}
openssl aes-256-cbc -K $ENCRYPTED_KEY -iv $ENCRYPTED_IV -in deploy_rsa.enc -out deploy_rsa -d
chmod 600 deploy_rsa
eval `ssh-agent -s`
ssh-add deploy_rsa

# Now that we're all set up, we can push.
git push -v -u origin $TARGET_BRANCH

# Go back to where we came from.
git checkout ${SOURCE_BRANCH}

## Now let's go have some fun with the cloned repo
#cd gh_pages_clone
#git config user.name "Travis CI"
#git config user.email "$COMMIT_AUTHOR_EMAIL"

## If there are no changes to the compiled out (e.g. this is a README update) then just bail.
#if [ -z `git diff --exit-code` ]; then
    #echo "No changes to the output on this push; exiting."
    #exit 0
#fi

# Commit the "changes", i.e. the new version.
# The delta will show diffs between new and old versions.
#git add .
#git commit -m "Deploy to GitHub Pages: ${SHA}"

## Get the deploy key by using Travis's stored variables to decrypt deploy_key.enc
#ENCRYPTED_KEY_VAR="encrypted_${ENCRYPTION_LABEL}_key"
#ENCRYPTED_IV_VAR="encrypted_${ENCRYPTION_LABEL}_iv"
#ENCRYPTED_KEY=${!ENCRYPTED_KEY_VAR}
#ENCRYPTED_IV=${!ENCRYPTED_IV_VAR}
#openssl aes-256-cbc -K $ENCRYPTED_KEY -iv $ENCRYPTED_IV -in deploy_rsa.enc -out deploy_rsa -d
#chmod 600 deploy_rsa
#eval `ssh-agent -s`
#ssh-add deploy_rsa

## Now that we're all set up, we can push.
#git push $SSH_REPO $TARGET_BRANCH

# based on https://gist.github.com/domenic/ec8b0fc8ab45f39403dd

#!/bin/bash
set -e # Exit with nonzero exit code if anything fails

# check python version
if [ "$DEPLOY_DOCS_FOR_PYTHON" != "$TRAVIS_PYTHON_VERSION" ]; then
    echo "Skipping deploy for python " $TRAVIS_PYTHON_VERSION
    exit 0
fi


SOURCE_BRANCH="master"
TARGET_BRANCH="gh-pages"

#path to gh-pages content
CONTENT="$VIRTUAL_ENV/share/doc/simex"

# path to encrypted secret key
KEY=$TRAVIS_BUILD_DIR/TravisCI/key

# Pull requests and commits to other branches shouldn't try to deploy, just build to verify
if [ "$TRAVIS_PULL_REQUEST" != "false" -o "$TRAVIS_BRANCH" != "$SOURCE_BRANCH" ]; then
    echo "Skipping deploy;"
    exit 0
fi

# Save some useful information
REPO=`git config remote.origin.url`
SSH_REPO=${REPO/https:\/\/github.com\//git@github.com:}
SHA=`git rev-parse --verify HEAD`
EMAIL=`git log -1 --pretty='%aE'`
NAME=`git log -1 --pretty='%aN'`

# Clone the existing branch
# we assume $TARGET_BRANCH exists
git clone -b $TARGET_BRANCH --single-branch $REPO ghpages_content

# Clean out existing contents
rm -rf ghpages_content/* || exit 0

# fill content with newly generated one
cp -r $CONTENT/* ghpages_content/


# Now let's go have some fun with the cloned repo
cd ghpages_content
# Create the .nojekyll file
touch .nojekyll

# set real user name and email
git config user.name  $NAME
git config user.email $EMAIL

# If there are no changes to the compiled then just bail.
if [ -z `git diff --exit-code` ] && [ -z `git ls-files --other --directory --exclude-standard` ]; then
    echo "No changes to the output on this push; exiting."
    exit 0
fi

# Commit the "changes", i.e. the new version.
git add -A .
git commit -m "Deploy to GitHub Pages: ${SHA}"

openssl aes-256-cbc -K $encrypted_1486bac6f46b_key -iv $encrypted_1486bac6f46b_iv -in $KEY -out deploy_key -d
chmod 600 deploy_key
eval `ssh-agent -s`
ssh-add deploy_key

# Now that we're all set up, we can push.
git push $SSH_REPO $TARGET_BRANCH


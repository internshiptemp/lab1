#!/bin/bash

# TODO: If these commands can be made to work (requires auth)
#       then we can use the push to notify students of their
#       test-case status.

git config -l

# git config --global user.email "stuarthoye@gmail.com"
# git config --global user.name "stuarthoye"
# git config --global github.user "stuarthoye"
# git config --global github.password $GIT_TOKEN

# git config -l

# git add ./.travis/diagnostics/
# git commit -m "Responding with test case results."
# git config --global push.default matching

# https://gist.github.com/mintindeed/4600385
# https://stackoverflow.com/questions/1335815/how-to-slice-an-array-in-bash
# UNAME="stuarthoye"
# PWORD=$GIT_TOKEN
# URL=$(git remote get-url --push origin)
# AUTH_URL="https://$UNAME:$PWORD@${URL[@]:8}"
# git push $AUTH_URL

# git config remote.origin.url $URL


echo $PRIVATE
echo $PUBLIC

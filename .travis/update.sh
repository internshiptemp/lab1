#!/bin/bash

# TODO: If these commands can be made to work (requires auth)
#       then we can use the push to notify students of their
#       test-case status.

echo "!!!"
echo "$GIT_TOKEN"
echo "!!!"

AUTH_ID="stuarthoye"
git config --global user.email "stuarthoye@gmail.com"
git config --global user.name "stuarthoye"
git config --global github.user "stuarthoye"
git config --global github.token $GIT_TOKEN

URL=$(git remote get-url origin)
echo $URL
NEWURL="${URL[@]:0:8}$AUTH_ID:$GIT_TOKEN@${URL[@]:8}"
echo $NEWURL

git config remote.origin.url $NEWURL

git add ./.travis/diagnostics/
git commit -m "Responding with test case results."
git config --global push.default matching
git push

git config remote.origin.url $URL

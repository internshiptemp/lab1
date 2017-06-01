#!/bin/bash

# TODO: If these commands can be made to work (requires auth)
#       then we can use the push to notify students of their
#       test-case status.

# How to stop Travis building and entering into an endless loop.
# https://coderwall.com/p/f7fusq/how-to-skip-making-a-build-in-travis-ci

# UNAME & PWORD are set within Travis as environment variables
echo $UNAME
echo $PWORD
URL=$(git config remote.origin.url)
AUTH_URL="https://$UNAME:$PWORD@${URL[@]:8}"

cp ./.travis/diagnostics/output ./output
git add ./output
git commit -m "Responding with test case results. [ci skip]"

# https://gist.github.com/mintindeed/4600385
# https://stackoverflow.com/questions/1335815/how-to-slice-an-array-in-bash
echo $AUTH_URL
git push $AUTH_URL

# git config remote.origin.url $URL


echo $PRIVATE
echo $PUBLIC

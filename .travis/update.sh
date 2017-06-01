#!/bin/bash

# TODO: If these commands can be made to work (requires auth)
#       then we can use the push to notify students of their
#       test-case status.

# How to stop Travis building and entering into an endless loop.
# https://coderwall.com/p/f7fusq/how-to-skip-making-a-build-in-travis-ci
# Scripting in Bash for Git
# https://gist.github.com/mintindeed/4600385
# https://stackoverflow.com/questions/1335815/how-to-slice-an-array-in-bash

UNAME="stuarthoye"
PWORD="80a50313f043efa0d83982c0293545ed3119727b"

# UNAME & PWORD are set within Travis as environment variables
# UNAME & PWORD are used to authenticate with github in order to permit a push
echo $UNAME
echo $PWORD
echo $PRIVATE
echo $PUBLIC


URL=$(git config remote.origin.url)
AUTH_URL="https://$UNAME:$PWORD@${URL[@]:8}"

echo $AUTH_URL

git config --global push.default simple

cp ./.travis/diagnostics/output ./output
cat ./output
git add ./output
git commit -m "Responding with test case results. [ci skip]"
git push $AUTH_URL



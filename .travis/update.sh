#!/bin/bash

# TODO: If these commands can be made to work (requires auth)
#       then we can use the push to notify students of their
#       test-case status.

git config --global github.user stuarthoye
git config --global github.token $GIT_TOKEN
git add ./travis/diagnostics/
git commit -m "Responding with test case results."
git config --global push.default matching
git push

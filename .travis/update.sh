#!/bin/bash

# TODO: If these commands can be made to work (requires auth)
#       then we can use the push to notify students of their
#       test-case status.

git config -l

git config --global user.email "stuarthoye@gmail.com"
git config --global user.name "stuarthoye"
git config --global github.user "stuarthoye"
git config --global github.password $GIT_TOKEN

git config -l

git add ./.travis/diagnostics/
git commit -m "Responding with test case results."
git config --global push.default matching
git push origin master

# git config remote.origin.url $URL

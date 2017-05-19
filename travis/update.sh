#!/bin/bash

git add ./travis/diagnostics/
git commit -m "Responding with test case results."
git config --global push.default matching
git push

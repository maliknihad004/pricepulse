#!/bin/bash

read -p "Branch to push: " branch
read -p "Commit message: " msg

git add .
git commit -m "$msg"
git push origin "$branch"
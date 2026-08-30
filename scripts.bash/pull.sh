#!/bin/bash

read -p "Branch to pull: " branch

git pull origin "$branch"
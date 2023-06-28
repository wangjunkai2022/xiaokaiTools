#!/bin/sh
#mac重置smartgit的试用
cd ~/Library/Preferences/SmartGit/
fils=$(ls)
for filename in $fils; do
  if [ -d "$filename" ]; then
    cd $filename
    rm -rf license
    rm -rf preferences.yml
  fi
done

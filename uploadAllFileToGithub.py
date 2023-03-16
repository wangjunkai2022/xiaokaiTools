#!/usr/bin/python3
from git.repo import Repo

gitPath = input()
print(gitPath)
repo = Repo(gitPath)
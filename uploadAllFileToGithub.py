#!/usr/bin/python3
# git文件夹下所有文件一个一个上传到git
import os
import sh
import re

exclude = [
]
gitPath = input()
# gitPath = "/Users/evan/codes/Other/OtherGit/Tool/"
print(gitPath)
os.chdir(gitPath)
print(sh.git("reset", "--soft", "HEAD^"))  # 取消git comment
rules = sh.git("status")  # 获取改动
all = re.findall(r"\t(.+?)\n", rules)  # 获得所有改动的文件
for file in all:
    isExclude = False
    for exc in exclude:
        if file.find(exc):
            isExclude = True
            continue
    if isExclude:
        print("此文件匹配排除列表中的文件 所有不上传：：：" + file)
        continue
    print("添加文件到github：" + file)
    print(sh.git("add", file))
    print(sh.git("commit", "-m", "Auto ADD File:" + file))
    print(sh.git("pull", "origin", "main"))
    print(sh.git("push", "origin", "main"))

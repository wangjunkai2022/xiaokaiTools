#!/usr/bin/python3
# git文件夹下所有文件一个一个上传到git
import os
import sh
import re

exclude = [
    ".DS_Store",
]


class AutoUpGit:
    def __init__(self, path):
        if not path[len(path) - 1] == "/":
            path = path + "/"
        os.chdir(path)

    def run(self):
        print("当前工作路径是：：" + os.getcwd())
        try:
            print(sh.git("reset", "--mixed", "HEAD^"))  # 取消git comment 和取消add（暂存）
        except Exception as ex:
            print(ex)
            print("没有文件需要重置提交")
        try:
            print(sh.git("pull", "origin", "main"))
        except Exception as ex:
            print(ex)
            err = ex.stderr.decode("utf-8")
            if err and "Please move or remove them before you merge." in err:
                all = re.findall(r"\t(.+?)\n", err)  # 获得所有改动的文件
                for file in all:
                    print("正在删除文件:" + file)
                    os.remove(file)
        rules = sh.git("status")  # 获取改动
        all = re.findall(r"\t(.+?)\n", rules)  # 获得所有改动的文件
        for file in all:
            isExclude = False
            for exc in exclude:
                if file.find(exc) != -1:
                    isExclude = True
                    continue
            if isExclude:
                print("此文件匹配排除列表中的文件 所有不上传：：：" + file)
                continue
            # newIndex = file.index("new file:")
            # if newIndex != -1:
            #     file = (file[file.index("new file:") + len("new file:"):len(file)]).strip()
            print("添加文件到github:" + file)
            print(sh.git("add", file))
            print(sh.git("commit", "-m", "Auto ADD File:" + file))
            print(sh.git("pull", "origin", "main"))
            print(sh.git("push", "origin", "main"))
        print("完成！！！！！！")


if __name__ == '__main__':
    print("请输入git文件路径")
    gitPath = input().strip()
    # gitPath = "/Users/evan/codes/Other/AV_Video"
    if gitPath is None or gitPath == "":
        gitPath = "./"
    if not gitPath[len(gitPath) - 1] == "/":
        gitPath = gitPath + "/"
    # print(gitPath)
    # os.chdir(gitPath)
    AutoUpGit(gitPath).run()

#!/usr/bin/python3
import time

import argparse
import git
import re

exclude = [
    ".DS_Store",
]


class GitAuto:
    remote = "origin"  # 远程仓库名称

    def __init__(self, repo_path: str = "./"):
        self.repo = git.Repo.init(repo_path)
        branches = [ref.name for ref in self.repo.refs if ref.name.startswith(self.remote)]

        #
        pattern = re.compile(r"{}/".format(self.remote))
        self.branches = [pattern.sub("", s) for s in branches]  # 所有远程分支
        self.branch_name = self.repo.active_branch.name
        self.print_active_branch_name()

    # 显示所有远程分支
    def show_all_branches(self):
        print("当前的所有远程分支")
        for index, branch in enumerate(self.branches):
            print(f"{index + 1}. {branch}")
        return self.branches

    # 设置当前操作的分支(已存在的远程分支)
    def set_branch_index(self, index: int):
        if index < 0 or index > len(self.branches):
            print("选择了一个不存在的分支 故使用当前{}分支".format(self.branch_name))
            return
        self.branch_name = self.branches[index + 1]
        if self.branch_name in self.repo.branches:
            self.repo.git.checkout(self.branch_name)
        else:
            self.repo.git.checkout('-b', self.branch_name, '{}/{}'.format(self.remote, self.branch_name))

    # 更具名字切换和创建分支
    def set_branch_name(self, name: str):
        if name == "" or not name:
            print("选择了一个不存在的分支 故使用当前{}分支".format(self.branch_name))
            return
        self.branch_name = name
        if not (self.branch_name in self.branches):  # 没有远程分支 创建
            local_branch = self.repo.create_head(self.branch_name)
            remote = self.repo.remote(self.remote)
            remote.push(refspec='{}:{}'.format(local_branch,
                                               # remote.name + '/' + 
                                               self.branch_name),
                        u=True, set_upstream=True)

        self.repo.git.checkout(self.branch_name)  # 切换分支到此分支

    # 重置所有没有push的提交
    def reset(self):
        self.repo.git.reset('--hard')
        # repo.git.push('-f', 'origin', 'master')

    # 增加提交文件
    def add_and_commit(self, items: []):
        self.repo.index.add(items)
        commit_str = "添加文件：\n"
        for file in items:
            commit_str = commit_str + file + "\n"
        self.repo.index.commit(commit_str)

    # 推送到服务器
    def push_all_commit(self):
        self.repo.remote(name=self.remote).push()

    def print_active_branch_name(self):
        print("当前分支是：{}".format(self.branch_name))

    # 添加所有改变文件到提交并推送(一个一个上传)
    def add_all_changes_2_commit(self):
        for file in self.repo.untracked_files:
            print("上传文件:{} 到git服务器中。。。。".format(file))
            isExclude = False
            for exc in exclude:
                if file.find(exc) != -1:
                    isExclude = True
                    continue
            if isExclude:
                print("此文件匹配排除列表中的文件 所以不上传：：：" + file)
                continue
            self.add_and_commit([file])
            self.push_all_commit()
            print("上传文件:{} 到git服务器完成".format(file))
            time.sleep(2)
            # break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', help='输入需要操作的git路径')
    if not parser.parse_args().path:
        print("请输入git文件路径")
        gitPath = input().strip()
    else:
        gitPath = parser.parse_args().path
    # gitPath = "/Users/evan/codes/Other/AV_Video"
    if gitPath is None or gitPath == "":
        gitPath = "./"
    if not gitPath[len(gitPath) - 1] == "/":
        gitPath = gitPath + "/"
    git_auto = GitAuto(gitPath)
    git_auto.show_all_branches()
    print("请输入需要操作的分支")
    # index = input().strip()
    # git_auto.set_branch_index(int(index))

    input_str = input().strip()
    if input_str.isdigit() or (input_str.startswith("-") and input_str[1:].isdigit()):
        print("输入为数字")
        git_auto.set_branch_index(int(input_str))
    else:
        print("输入为字符")
        git_auto.set_branch_name(input_str)

    git_auto.add_all_changes_2_commit()
    # git_auto.push_all_commit()

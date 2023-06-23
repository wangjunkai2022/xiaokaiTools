#!/usr/bin/python3
import argparse
import git
import os


class GitPull:
    def __init__(self, path, url=None, username=None, password=None):
        if os.path.exists(path + '/.git'):
            self.repo = git.Repo(path)
        else:
            # url = "https://kaikai2024:Xiaokai2022@gitee.com/kaikai2024/video.git"
            # username = input("Please input the git username: ")
            # password = input("Please input the git password: ")
            self.repo = git.Repo.clone_from(url, path, depth=1)
        self.branches = self.repo.branches
        self.selected_branch = None

    def list_branches(self):
        print("Branches:")
        for index, branch in enumerate(self.branches):
            print(f"{index + 1}. {branch}")

    def select_branch(self, index):
        self.selected_branch = list(self.branches)[index - 1]

    def pull_files(self):
        for file in self.selected_branch.commit.tree:
            if os.path.exists(file.name):
                print(f"Skip {file.name}")
            else:
                print(f"Pulling {file.name}")
                self.repo.git.checkout(self.selected_branch)
                self.repo.git.pull()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', help='输入需要操作的git路径')
    parser.add_argument('--git', help='git远程路径')
    parser.add_argument('--username', help='git远程用户名')
    parser.add_argument('--password', help='git远程用户名的密码')
    args = parser.parse_args()
    gitPath = parser.parse_args().path
    if not gitPath:
        print("请输入git文件路径")
        gitPath = input().strip()
    # gitPath = "/Users/evan/codes/Other/AV_Video"
    if gitPath is None or gitPath == "":
        gitPath = "./"
    if not gitPath[len(gitPath) - 1] == "/":
        gitPath = gitPath + "/"
    # if not parser.parse_args().git:
    git_pull = GitPull(gitPath, url=args.git, username=args.username, password=args.password)
    git_pull.list_branches()
    index = int(input("Please select a branch: "))
    git_pull.select_branch(index)
    git_pull.pull_files()

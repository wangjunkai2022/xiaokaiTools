#!/usr/bin/python3
import os
import subprocess
import sys, getopt


def main(argv):
    dir = None
    cmd = ""
    suffix = ""
    try:
        opts, args = getopt.getopt(argv, "c:d:s:", ["cmd=", "dir=", "suffix="])
    except getopt.GetoptError:
        print("runAllFile -c[--cmd] 需要运行的命令 -d[--dir] 更目录 -s[--suffix] 指定的后缀的文件")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-c', "--cmd"):
            cmd = arg
        elif opt in ("-d", "--dir"):
            dir = arg
        elif opt in ("-s", "--suffix"):
            suffix = arg
    # print(dir, cmd, suffix)

    for file in os.listdir(dir):
        if os.path.splitext(file)[1] == "":
            continue
        if os.path.splitext(file)[1] in suffix:
            file_path = dir + "/" + file
            # print(file_path)
            print(subprocess.call([cmd, file_path], shell=False))


if __name__ == '__main__':
    main(sys.argv[1:])

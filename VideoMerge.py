#!/usr/bin/python3
# 合并多个mp4文件为1个
import argparse
import os
import subprocess

my_env = {'PATH': '/usr/local/bin'}


class mp4merge:
    def __init__(self, folder_path, file_name):
        self.folder_path = folder_path
        self.file_name = file_name

    def merge(self):
        # 获取指定文件夹中所有MP4文件
        files = [f for f in os.listdir(self.folder_path) if
                 f.endswith('.mp4') and f.startswith(self.file_name) and (f != self.file_name + '.mp4')]
        if len(files) < 2:
            print('No MP4 files found in the folder.')
            return

        # 按文件名排序
        files.sort()
        concat = "concat:"
        ts_files = []
        for f in files:
            tempName = os.path.basename(f) + "_temp.ts"
            cmd = [
                'ffmpeg', '-i', os.path.join(self.folder_path, f), '-c', 'copy', '-bsf:v', 'h264_mp4toannexb', '-f',
                'mpegts',
                tempName,
            ]
            subprocess.call(cmd, env=my_env)
            concat += tempName + "|"
            ts_files.append(tempName)

        subprocess.call(['ffmpeg', '-i',
                         concat,
                         '-c', 'copy',
                         # "-absf", 'aac_adtstoasc',
                         os.path.join(self.folder_path, self.file_name + '.mp4')], env=my_env)
        for file in ts_files:
            os.remove(file)
        print(
            "文件\n{}\n已经全部合并到文件\n{}\n"
                .format(
                files, self.file_name + '.mp4')
        )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', help='需要合并的文件夹路径 默认为当前目录', default="./")
    parser.add_argument('--name', help='开始文件名', default="")
    args = parser.parse_args()
    mp4merge(args.path, args.name).merge()

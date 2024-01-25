# 此文件 删除指定位置的重复文件 找到视频中大小为0的文件
import time
import asyncio
import os
import re
import shutil
import sehuatang
import alist
import pikpak
import video
import nfo

vidoe_suffix = [
    'mp4',
    'avi',
    'mkv',
    'mpg',
    "mpeg",
    "rm",
    "rmvb",
    "mov",
    "wmv",
    'flv',
]


def is_video(file):
    file_name, file_houzui = get_file_names(file)
    for su in vidoe_suffix:
        if file_houzui == su:
            return True
    return False


def get_file_names(file):
    file_name = os.path.splitext(file)[0]
    file_houzui = os.path.splitext(file)[-1][1:]
    return file_name, file_houzui


def main(path):
    files_size_zero = video.getSizeZeroVides(path)  # 大小是0的视频文件

    # 新下载所有大小为0的视频
    for all_path_file in files_size_zero:
        # 父文件夹路径
        parent_path = os.path.abspath(os.path.join(all_path_file, "../"))
        # file = all_path_file[len(parent_path) + 1:]  # 不包含全路径的文件
        # file_name, file_houzui = get_file_names(file)
        av_number = os.path.basename(parent_path)
        # print(file_name)
        loop = asyncio.get_event_loop()
        #  更具番号搜索
        get_future = asyncio.ensure_future(sehuatang.SearchNumberToMagnets(av_number))  # 相当于开启一个future
        loop.run_until_complete(get_future)  # 事件循环
        magnets = get_future.result()
        print("当前{}下搜索到的下载BT:{}".format(av_number, magnets))  # 获取结果
        # pikpakPath = parent_path.replace("/data/videos/media/alist/PikPak2/", "")
        pikapk_re = re.search(r"PikPak.*?/", parent_path)
        pikpakPath = parent_path[pikapk_re.end():]
        for magnet in magnets:
            pikpak_future = asyncio.ensure_future(
                pikpak.officeDownload(magnet, pikpakPath))  # 相当于开启一个future
            loop.run_until_complete(pikpak_future)  # 等待结束
            download_name = pikpak_future.result()
            time.sleep(5)
            alist_re = re.search(r"alist/", parent_path)
            alist_path = parent_path[alist_re.end():]
            print("刷新alist的文件夹")
            loop.run_until_complete(asyncio.ensure_future(alist.update_all(alist_path)))

            new_dir_path = os.path.join(parent_path, download_name)
            while not os.path.exists(new_dir_path):
                print("文件已经下载完成怎么会没有呢？？？")
                print("等待10秒在看看")
                time.sleep(10)
                # loop.run_until_complete(asyncio.ensure_future(alist.update_all(alist_path)))

            videos = video.getReNameParentVideo(new_dir_path, av_number)
            for video_file in videos:
                old_video_path = os.path.join(parent_path, video_file)  # 需要移动到的目录
                src_path = os.path.join(new_dir_path, video_file)  # 下载的新文件的位置
                if os.path.exists(old_video_path) and os.path.getsize(old_video_path) < os.path.getsize(src_path):
                    while os.path.exists(old_video_path):  # 无需循环检测需要复制到的目录下是否存在相同名字的文件 如果有删除 没有则跳过
                        time.sleep(2)
                        print("删除旧文件\n{}".format(old_video_path))
                        try:
                            os.remove(old_video_path)
                        except Exception as e:
                            print("删除 {} 文件错误\n错误码:\n{}".format(old_video_path, e))
                        time.sleep(5)

                while not os.path.exists(old_video_path):
                    time.sleep(2)
                    print("开始移动文件\n{}\n到\n{}".format(src_path, old_video_path))
                    try:
                        shutil.move(src_path, old_video_path)
                    except Exception as e:
                        print("移动 {} 文件错误\n错误码:\n{}".format(src_path, e))
                    time.sleep(5)

                # nfo 文件操作
                nfo.nfo(old_video_path)
                time.sleep(5)
            while os.path.exists(all_path_file) and os.path.getsize(all_path_file) == 0 and len(videos) > 0:
                print("删除原来大小为0的文件\n{}".format(all_path_file))
                try:
                    os.remove(all_path_file)
                except Exception as e:
                    print("删除原来大小为0的文件错误\n错误码:\n{}".format(all_path_file, e))
                time.sleep(5)

            print("在视频移动完成后删除下载的文件夹")
            while os.path.isdir(new_dir_path) and os.path.exists(new_dir_path):
                try:
                    shutil.rmtree(new_dir_path)
                except Exception as e:
                    print("删除下载的文件夹\n{}\n错误码:{}".format(new_dir_path, e))
                    time.sleep(10)
                time.sleep(1)
        while os.path.exists(all_path_file) and len(
                video.getReNameParentVideo(parent_path, av_number)) >= 2 and os.path.getsize(all_path_file) == 0:
            try:
                os.remove(all_path_file)
            except Exception as e:
                print("删除\n{}\n错误".format(all_path_file))
            time.sleep(5)
    files_repeat = video.getFileNameRepeats(path)  # 相同的文件

    for file in files_repeat:
        os.remove(file)
        print("删除重复文件：{}".format(file))


if __name__ == '__main__':
    # path = "/data/videos/media/alist/PikPak2/整理/中文字幕无码破解/希島あいり/"
    path = "/data/videos/media/alist/PikPak2/整理"
    main(path)

# 此文件 删除指定位置的重复文件 找到视频中大小为0的文件
import sys
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
import datetime
import logging

logging.basicConfig(level=logging.INFO)
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

PIKPAK_PATH = "/Volumes/dav/色花堂无码无破解/"
ALIST_PATH = "dav/"


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


def create_null_dir(path):
    if sys.platform.startswith("win"):
        logging.info("当前系统是Windows")
    elif sys.platform.startswith("linux"):
        logging.info("当前系统是Linux")
    elif sys.platform.startswith("darwin"):
        logging.info("当前系统是Mac OS")
        if os.path.exists(path) and os.path.isdir(path):
            test_dir = os.path.join(path, "test")
            结果 = os.popen(f'mkdir {test_dir}').read()
            logging.info(f"创建空文件夹\n{test_dir}\n结果:{结果}")
            time.sleep(2)
            结果 = os.popen(f'rm -rf {test_dir}').read()
            logging.info(f"删除空文件夹\n{test_dir}\n结果:{结果}")
        else:
            next_path = os.path.abspath(path)
            create_null_dir(next_path)
    else:
        logging.info(f"这里不知什么系统:{sys.platform}")


def main(path):
    files_size_zero = []
    size_zero_txt_file_path = os.path.abspath(os.path.dirname(__file__)) + "/zero_file.txt"
    if os.path.exists(size_zero_txt_file_path):
        with open(size_zero_txt_file_path, "r") as f:
            files_size_zero = f.read().split("\n")

    if len(files_size_zero) == 0:
        files_size_zero = video.getSizeZeroVides(path)  # 大小是0的视频文件
        # files_size_zero = []  # 大小是0的视频文件
        for zero_file in files_size_zero:
            with open(os.path.abspath(os.path.dirname(__file__)) + "/zero_file.txt", "a") as f:
                f.write(zero_file + "\n")

    # 新下载所有大小为0的视频
    for all_path_file in files_size_zero:
        if not os.path.exists(all_path_file) or os.path.getsize(all_path_file) > 0:
            continue
        # 父文件夹路径
        parent_path = os.path.abspath(os.path.join(all_path_file, "../"))
        # file = all_path_file[len(parent_path) + 1:]  # 不包含全路径的文件
        # file_name, file_houzui = get_file_names(file)
        av_number = os.path.basename(parent_path)
        # logging.info(file_name)
        loop = asyncio.get_event_loop()
        #  更具番号搜索
        get_future = asyncio.ensure_future(sehuatang.SearchNumberToMagnets(av_number))  # 相当于开启一个future
        loop.run_until_complete(get_future)  # 事件循环
        magnets = get_future.result()
        logging.info("当前{}下搜索到的下载BT:{}".format(av_number, magnets))  # 获取结果
        # pikpakPath = parent_path.replace("/data/videos/media/alist/PikPak2/", "")
        pikapk_re = re.search(PIKPAK_PATH, parent_path)
        pikpakPath = parent_path[pikapk_re.end():]
        for magnet in magnets:
            pikpak_future = asyncio.ensure_future(
                pikpak.officeDownload(magnet, pikpakPath))  # 相当于开启一个future
            loop.run_until_complete(pikpak_future)  # 等待结束
            download_name = pikpak_future.result()
            logging.info(f"下载文件到pikpak的文件名字{download_name}")
            if not download_name or download_name == "":
                # 获取当前时间
                now_time = datetime.datetime.now()
                # 格式化时间字符串
                str_time = now_time.strftime("%Y-%m-%d %H:%M:%S")
                error_str = (f"{str_time}:这里等待时下载失败\nmagnet:{magnet}\nparent_path:{parent_path}\n")
                with open(os.path.abspath(os.path.dirname(__file__)) + "/下载失败.log", "a") as f:
                    f.writelines(error_str)
                logging.error(error_str)
                continue
            time.sleep(5)
            alist_re = re.search(ALIST_PATH, parent_path)
            alist_path = parent_path[alist_re.end():]
            logging.info("刷新alist的文件夹")
            loop.run_until_complete(asyncio.ensure_future(alist.update_all(alist_path)))

            new_dir_path = os.path.join(parent_path, download_name)
            index_count = 0
            while not os.path.exists(new_dir_path):
                index_count += 1
                logging.info("文件已经下载完成怎么会没有呢？？？")
                logging.info("等待10秒在看看")
                logging.error(f'文件{new_dir_path}离线现在成功 但是在文件系统中没有找到 这里等待10秒在重试')
                time.sleep(10)
                if index_count >= 5:
                    index_count = 0
                    create_null_dir(parent_path)
                    loop.run_until_complete(asyncio.ensure_future(alist.update_all(alist_path)))
                    logging.error(f'文件{new_dir_path}在文件系统中查找多次失败 调用系统的创建空test文件夹')

            videos = video.getReNameParentVideo(new_dir_path, av_number)
            for video_file in videos:
                old_video_path = os.path.join(parent_path, video_file)  # 需要移动到的目录
                src_path = os.path.join(new_dir_path, video_file)  # 下载的新文件的位置
                if os.path.exists(old_video_path) and os.path.getsize(old_video_path) < os.path.getsize(src_path):
                    while os.path.exists(old_video_path):  # 无需循环检测需要复制到的目录下是否存在相同名字的文件 如果有删除 没有则跳过
                        time.sleep(2)
                        logging.info("删除旧文件\n{}".format(old_video_path))
                        try:
                            os.remove(old_video_path)
                        except Exception as e:
                            logging.info("删除 {} 文件错误\n错误码:\n{}".format(old_video_path, e))
                        time.sleep(5)

                index_count = 0
                while not os.path.exists(old_video_path):
                    time.sleep(2)
                    logging.info("开始移动文件\n{}\n到\n{}".format(src_path, old_video_path))
                    try:
                        shutil.move(src_path, old_video_path)
                    except Exception as e:
                        logging.error("移动 {} 文件错误\n错误码:\n{}".format(src_path, e))
                    time.sleep(5)
                    alist_re = re.search(ALIST_PATH, parent_path)
                    alist_path = parent_path[alist_re.end():]
                    loop.run_until_complete(asyncio.ensure_future(alist.update_all(alist_path)))
                    index_count += 1
                    if index_count >= 5:
                        index_count = 0
                        logging.error(f"{old_video_path}多次移动文件失败 这里调用系统的创建空文件夹")
                        create_null_dir(src_path)

                # nfo 文件操作
                nfo.nfo(old_video_path)
                time.sleep(5)

            index_count = 0
            while os.path.exists(all_path_file) and os.path.getsize(all_path_file) == 0 and len(videos) > 0:
                logging.info("删除原来大小为0的文件\n{}".format(all_path_file))
                try:
                    os.remove(all_path_file)
                except Exception as e:
                    logging.error("删除原来大小为0的文件错误\n错误码:\n{}".format(all_path_file, e))
                time.sleep(5)
                index_count += 1
                if index_count >= 5:
                    index_count = 0
                    logging.error(f"{all_path_file}删除原来大小为0的文件失败 这里调用系统的创建空文件夹")
                    create_null_dir(all_path_file)

            logging.info(f"在视频移动完成后删除下载的文件夹:\n{new_dir_path}")
            if new_dir_path == parent_path:
                logging.error(f"需要删除的文件夹是原文件路径 这里不删除:\n{new_dir_path}")
                continue
            while os.path.isdir(new_dir_path) and os.path.exists(new_dir_path):
                try:
                    shutil.rmtree(new_dir_path)
                except Exception as e:
                    logging.error("删除下载的文件夹\n{}\n错误码:{}".format(new_dir_path, e))
                    time.sleep(10)
                time.sleep(1)

        while os.path.exists(all_path_file) and len(
                video.getReNameParentVideo(parent_path, av_number)) >= 2 and os.path.getsize(all_path_file) == 0:
            try:
                os.remove(all_path_file)
            except Exception as e:
                logging.info("删除\n{}\n错误".format(all_path_file))
            time.sleep(5)
    if os.path.exists(size_zero_txt_file_path):
        os.remove(size_zero_txt_file_path)

    logging.info("大小是0的视频文件处理完毕")
    logging.info("开始查找相同文件")
    files_repeat = video.getFileNameRepeats(path)  # 相同的文件
    for file in files_repeat:
        os.remove(file)
        logging.info("删除重复文件：{}".format(file))

    logging.info("开始查找隐藏文件")
    for file in video.getDotStartFiles(path):  # 隐藏文件
        os.remove(file)
        logging.info("删除隐藏文件：{}".format(file))


if __name__ == '__main__':
    # path = "/data/videos/media/alist/PikPak2/整理/中文字幕无码破解/希島あいり/"
    path = "/Volumes/dav/色花堂无码无破解/JAV_output"
    # path = "/Volumes/dav/sehuatang1/整理"  # 需要整理的文件夹
    # PIKPAK_PATH = "/Volumes/dav/sehuatang1/"  # pikpak 的路径
    # alist_path = "/Volumes/dav/"
    main(path)

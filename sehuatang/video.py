import os
import re


# 获取名字符合父文件夹名字的视频文件名
def getReNameParentVideo(path, re_name):
    from Organize_Files import is_video
    _videos = []
    if os.path.isdir(path):
        # parent_path = os.path.abspath(os.path.join(path, '../'))
        # print("parent_path" + parent_path)
        # dir_name = os.path.basename(parent_path)
        for file in os.listdir(path):
            if is_video(file):
                file_re = re.search(re_name, file, re.IGNORECASE)
                if file_re:
                    _videos.append(file)
    return _videos


# 获取文件大小为0的视频文件
def getSizeZeroVides(path):
    from Organize_Files import is_video
    files_size_zero = []
    for root, dir, files in os.walk(path):
        # print(files)
        for file in files:
            if is_video(file):
                file_path = os.path.join(root, file)
                size = os.path.getsize(file_path)
                # print("文件大小:{}".format(size))
                if size == 0:
                    files_size_zero.append(file_path)
    return files_size_zero


# 获取文件夹下所有以.开头的文件和.DS_Store 文件
def getDotStartFiles(path):
    from Organize_Files import get_file_names
    files_repeat = []  # 文件名中包含（.开头的文件）
    for root, dir, files in os.walk(path):
        # print(files)
        for file in files:
            file_name, file_houzui = get_file_names(file)
            if file_name.startswith(".") or "DS_Store" in file_name:
                files_repeat.append(os.path.join(root, file))

    return files_repeat


# 获取文件夹下名字重复的文件
def getFileNameRepeats(path):
    from Organize_Files import get_file_names
    files_repeat = []  # 文件名中包含（1位数字的文件）
    for root, dir, files in os.walk(path):
        # print(files)
        for file in files:
            file_name, file_houzui = get_file_names(file)
            # print("文件名是:{0},文件后缀是:{1}".format(file_name, file_houzui))
            mt = re.search(r"\(\d+\)", file_name)
            mt2 = re.search(r"-\d+", file_name)
            if mt:
                remove_repeat_name = file_name[0:mt.start()]
                remove_repeat_path = remove_repeat_name + "." + file_houzui
                file_path = os.path.join(root, file)
                if os.path.exists(os.path.join(root, remove_repeat_path)) and os.path.getsize(
                        os.path.join(root, remove_repeat_path)) == os.path.getsize(file_path):
                    files_repeat.append(file_path)
            elif mt2:
                remove_repeat_name = file_name[0:mt2.start()]
                remove_repeat_path = remove_repeat_name + "." + file_houzui
                file_path = os.path.join(root, file)
                if os.path.exists(os.path.join(root, remove_repeat_path)) and os.path.getsize(
                        os.path.join(root, remove_repeat_path)) == os.path.getsize(file_path):
                    __number = int(file_name[mt2.start():])
                    if __number and __number < -999:
                        files_repeat.append(file_path)
    return files_repeat


if __name__ == '__main__':
    # path = "/data/videos/media/alist/PikPak2/整理/中文字幕无码破解/希島あいり/IPZ-299"
    # videos = getReNameParentVideo(path, "IPZ-299")
    # print(videos)
    # path = "./"
    # files = getFileNameRepeats(path)
    # print(files)

    # path = "/data/videos/media/alist/PikPak2/整理"
    # path = "/data/videos/media/alist/JAV合集一/JAV合集一"
    path = "/Volumes/dav/SukebeiEnyo合集一"
    # path = "/Users/evan/codes/Other/Tools/sehuatang"
    files_repeat = getFileNameRepeats(path)  # 相同的文件

    for file in files_repeat:
        # os.remove(file)
        print("删除重复文件：{}".format(file))
    # print(files)

    # path=""
    # files = getReNameParentVideo(path)

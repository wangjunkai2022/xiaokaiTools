import time
import os
import shutil


def nfo(file):
    from Organize_Files import is_video
    from Organize_Files import get_file_names
    if not is_video(file):
        return
    # 文件所在文件夹
    video_all_name = os.path.basename(os.path.abspath(file))
    parent_all_path = os.path.abspath(os.path.join(file, '../'))
    parent_name = os.path.basename(parent_all_path)
    video_name, video_houzui = get_file_names(video_all_name)
    nfo_all_path = os.path.abspath(os.path.join(parent_all_path, video_name + ".nfo"))
    if os.path.exists(nfo_all_path):
        nfo_size = os.path.getsize(nfo_all_path)
        if nfo_size < 1 * 1024:
            # 删除原文件
            print("文件大小:\t{} \n删除原文件\n{}".format(nfo_size, nfo_all_path))
            while os.path.exists(nfo_all_path):
                try:
                    os.remove(nfo_all_path)
                except Exception as e:
                    print("{}\n文件删除错误\n{}".format(nfo_all_path, e))
                time.sleep(5)
            return __copy_size_max_nfo(nfo_all_path)
        else:
            return nfo_all_path
    else:
        return __copy_size_max_nfo(nfo_all_path)


def __copy_size_max_nfo(file):
    while os.path.exists(file):
        try:
            os.remove(file)
        except Exception as e:
            print("{}\n文件删除错误\n{}".format(file, e))
        time.sleep(5)
    from Organize_Files import get_file_names
    parent_all_path = os.path.abspath(os.path.join(file, '../'))
    nfos = []
    for _file in os.listdir(parent_all_path):
        name, houzui = get_file_names(_file)
        if houzui == "nfo":
            nfos.append(_file)
    nfos.sort(key=lambda value: os.path.getsize(os.path.abspath(os.path.join(parent_all_path, value))),
              reverse=True)
    while not os.path.exists(file) and len(nfos) > 0:
        try:
            _old_file = os.path.join(parent_all_path, nfos[0])
            print("开始复制文件\n{}\n到\n{}".format(_old_file, file))
            shutil.copy2(_old_file, file)
        except Exception as e:
            print("复制文件错误{}".format(e))
        time.sleep(5)
    return file


if __name__ == '__main__':
    path = "/data/videos/media/alist/PikPak2/整理/中文字幕无码破解/希島あいり/IPZ-299/IPZ-299-UC.mp4"
    videos = nfo(path)
    print(videos)
    path = "/data/videos/media/alist/PikPak2/整理/中文字幕无码破解/希島あいり/IPZ-299/IPZ-299.wmv"
    videos = nfo(path)
    print(videos)


from pikpakapi import PikPakApi, DownloadStatus
import asyncio

pikpak_username = "himiren433@picvw.com"
pikpak_pw = "poi098"
client = PikPakApi(pikpak_username, pikpak_pw)
checkCount = 10


# 离线下载文件到指定目录 返回下载好后的名字
async def officeDownload(magnet, path):
    print("下载磁力连接{}\n到pikpak\n{}".format(magnet, path))
    await client.login()
    # 获取pikpak的path的id
    paths = await asyncio.wait_for(client.path_to_id(path, True), timeout=50000)
    path_id = paths[len(paths) - 1].get("id", None)
    result = await asyncio.wait_for(client.offline_download(magnet, path_id), timeout=50000)
    task_id = result.get("task").get('id')
    file_id = result.get("task").get('file_id')
    file_name = result.get("task").get('file_name')
    status_count = 0
    while True:
        status_count += 1
        task = client.get_task_status(task_id, file_id)
        result = await asyncio.wait_for(task, timeout=10000)
        print("{} 的 下载状态：{}".format(file_name, result))
        if DownloadStatus.done == result or DownloadStatus.not_found == result:
            break
        await asyncio.sleep(2)
        if status_count >= checkCount:
            raise Exception(
                "检测{}次 还是未完成下载 这里判断为下载失败。。。。。。。".format(checkCount))

    print("pikpak 保存完成：{} 保存路径：{}".format(file_name, path))
    return file_name


if __name__ == '__main__':
    asyncio.run(officeDownload("magnet:?xt=urn:btih:4C31FFB4167CEC4239992202624065ACF86C5E82&dn=ipx-567-C",
                               "整理/中文字幕无码破解/希島あいり/IPZ-299"))

import os

from PyQt6RunShell import DownloadWidget, ShellWidget, ZipWidget

android_tools_path = "AndroidTools"


def _chaech_android_tools_path():
    if not os.path.exists(android_tools_path):
        os.mkdir(android_tools_path)


class ApkTool:
    def __init__(self, apk_file: str):
        self.apk = apk_file
        _chaech_android_tools_path()
        self.apktool = os.path.join(android_tools_path, "apktool_2.7.0.jar")
        self.apktool_url = "https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.7.0.jar"
        if not os.path.exists(self.apktool):
            dw = DownloadWidget(self.apktool_url, self.apktool)
            dw.run()

    def run(self):
        apk_name = os.path.splitext(self.apk)[0]
        # 使用apktool导出反编译工程
        shell = ShellWidget()
        apk_tools_dir_path = os.path.join(os.path.dirname(self.apk), apk_name)  # apk 反编译工程路径
        shell.run(["java", "-jar", self.apktool, "d", "-o", apk_tools_dir_path, self.apk])


class JadxTool:
    def __init__(self, apk_file: str):
        self.apk = apk_file
        _chaech_android_tools_path()
        self.jadx_path = os.path.join(android_tools_path, "jadx-1.4.7/bin/jadx")
        self.jadx_url = "https://github.com/skylot/jadx/releases/download/v1.4.7/jadx-1.4.7.zip"
        if not os.path.exists(self.jadx_path):
            dw = DownloadWidget(self.jadx_url, android_tools_path)
            dw.run()
            zw = ZipWidget(dw.file)
            zw.run()

    def run(self):
        apk_name = os.path.splitext(self.apk)[0]
        as_path = os.path.join(os.path.dirname(self.apk), apk_name + "_android_studio")  # 反编译AndroidStudio工程路径
        shell = ShellWidget()
        shell.run([self.jadx_path, "-e", "-d", as_path, self.apk])


# 软连接smali
class AndroidComToSmaliAs:
    def __init__(self, apk, com_path: str = None, as_path: str = None):
        if com_path is None or com_path == "" or com_path == " ":
            apk_name = os.path.splitext(apk)[0]
            self.com_path = os.path.join(os.path.dirname(apk), apk_name)
        else:
            self.com_path = com_path

        if as_path is None or as_path == "" or as_path == " ":
            apk_name = os.path.splitext(apk)[0]
            self.as_path = os.path.join(os.path.dirname(apk), apk_name + "_android_studio")
        else:
            self.as_path = as_path

        # 转相对路径为绝对路径
        if not os.path.isabs(self.as_path):
            self.as_path = os.path.abspath(self.as_path)
        if not os.path.isabs(self.com_path):
            self.com_path = os.path.abspath(self.com_path)
        pass

    def run(self):
        # 连接反编译工程的 smali 到AndroidStudio 的smails中
        as_smali_path = os.path.join(self.as_path, "app/src/main/smalis")
        if not os.path.exists(as_smali_path):
            os.mkdir(as_smali_path)
        smali_path = []
        for _path in os.listdir(self.com_path):
            if "smali" in _path:
                smali_path.append(_path)
        for smali in smali_path:
            _smali_path = os.path.join(self.com_path, smali)
            cmd = ["ln", "-s", _smali_path,
                   as_smali_path]  # 软连接源路径一定得是绝对路径
            # worker = WorkerShellRun(cmd)
            # self._thread_pool.start(worker)
            shell = ShellWidget()
            shell.run(cmd)

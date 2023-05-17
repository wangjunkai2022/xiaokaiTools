# !/usr/bin/python3
import os
import subprocess
import time
from enum import Enum
from PyQt6.QtCore import QObject, pyqtSignal, QEventLoop, QTimer, QEvent, QThread, QRunnable, QThreadPool
from PyQt6.QtGui import QTextCursor, QAction, QIcon
from PyQt6.QtWidgets import (QWidget, QPushButton, QLineEdit,
                             QInputDialog, QApplication, QFileDialog, QErrorMessage, QMessageBox, QMainWindow,
                             QTextEdit, QHBoxLayout, QLayout, QLabel, QVBoxLayout)
import sys

import uploadAllFileToGithub
from PyQt6AndroidTool import ApkTool, JadxTool, AndroidComToSmaliAs

from PyQt6RunShell import DownloadWidget, ZipWidget, ShellWidget


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.__initUI()
        sys.stdout = Stream(newText=self._onUpdateText)

    # 打印监听
    def _onUpdateText(self, text):
        """Write console output to text widget."""
        cursor = self.process.textCursor()
        # cursor.movePosition(QTextCursor.MoveOperation)
        cursor.insertText(text)
        self.process.setTextCursor(cursor)
        self.process.ensureCursorVisible()

    def __initUI(self):
        self.main_widget = QWidget()
        self._mainQVLayout = QVBoxLayout(self.main_widget)
        self.setLayout(self._mainQVLayout)
        self.setCentralWidget(self.main_widget)

        self._mainQVLayout.addWidget(AutoGitPush())
        self._mainQVLayout.addWidget(VideoToM3U8())
        self._mainQVLayout.addWidget(EncodeMp4Video())
        self._mainQVLayout.addWidget(DecodeMp4Video())
        self._mainQVLayout.addWidget(PlayMp4Video())
        self._mainQVLayout.addWidget(MacLnAndroid())
        self._mainQVLayout.addWidget(ApkDecompilation())

        self.process = QTextEdit(self, readOnly=True)
        self.process.ensureCursorVisible()
        self._clean_debug_btn = QPushButton("清除记录")
        self._clean_debug_btn.clicked.connect(lambda: self.process.setText(""))
        self._mainQVLayout.addWidget(self._clean_debug_btn)
        self._mainQVLayout.addWidget(self.process)

        self.setGeometry(300, 300, 450, 700)
        self.setWindowTitle('PyQt6_Tool_Windows')
        self.show()


# 文件选择枚举
class SelectFileType(Enum):
    # 文件
    File = 1
    # 文件夹
    Dir = 2
    # 视频文件
    VideoFile = 3
    # apk文件
    ApkFile = 4


class Stream(QObject):
    """Redirects console output to text widget."""
    newText = pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))


# 开启新线程执行cmd命令
class WorkerShellRun(QRunnable):
    def __init__(self, cmd):
        super(WorkerShellRun, self).__init__()
        self.cmd = cmd
        self._init()
        self.isOver = False
        self.__callback = None

    def _init(self):
        evn = os.environ.copy()
        evn["PATH"] = evn["PATH"] + ":/usr/local/bin"
        self.popen = subprocess.Popen(self.cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT, text=True, env=evn)

    def set_callback(self, callback):
        self.__callback = callback

    def run(self):
        while True:
            # time.sleep(0.5)
            out = self.popen.stdout.readline()
            if out != "":
                print(out)
            if out == '' and not self.popen.poll():
                print("执行完毕")
                self.isOver = True
                print(type(self.__callback))
                if self.__callback:
                    self.__callback()
                return

    # 关闭此线程
    def coles_shell(self):
        self.popen.kill()


# 显示一行和输入框的BaseWidget
class BaseLineWidget(QWidget):
    def __init__(self, name: str, input_str: str, file_type=SelectFileType.File):
        super(BaseLineWidget, self).__init__()
        self.horizontal_layout = QHBoxLayout()
        self._run_btn = QPushButton('开始')
        self.horizontal_layout.addWidget(QLabel(name))
        self.horizontal_layout.addWidget(self._run_btn)
        self.setLayout(self.horizontal_layout)
        self._run_btn.clicked.connect(self._run_btn_function)

        # 输入框
        self._url_path_txt = QLineEdit()
        self.horizontal_layout.addWidget(self._url_path_txt)
        self._url_path_txt.setPlaceholderText(input_str)
        self._url_path_txt.installEventFilter(self)
        self.__file_type = file_type
        self._thread_pool = QThreadPool()

    def _edit_text(self):
        txt = self._url_path_txt.text()
        if txt is None or txt == "":
            if self.__file_type == SelectFileType.File:
                dir, ok = QFileDialog.getOpenFileName(self)
                if ok:
                    self._url_path_txt.setText(dir)
            elif self.__file_type == SelectFileType.VideoFile:
                dir, ok = QFileDialog.getOpenFileName(self,
                                                      filter="视频文件(*.mp4 *.mkv *.wmv *.mov *.swf *.flv *.avi *.rm *.rma *.mpg *.mpeg)")
                if ok:
                    self._url_path_txt.setText(dir)
            elif self.__file_type == SelectFileType.ApkFile:
                dir, ok = QFileDialog.getOpenFileName(self,
                                                      filter="Apk文件(*.apk)")
                if ok:
                    self._url_path_txt.setText(dir)
            elif self.__file_type == SelectFileType.Dir:
                dir = QFileDialog.getExistingDirectory(self, "选择文件夹", "/")
                self._url_path_txt.setText(dir)
        else:
            pass

    # 重写这个方法 运行命令 path是当前选中执行命令文件选中的路径
    def run_shell(self, path):
        pass

    def _run_btn_function(self):
        text = self._url_path_txt.text()
        if text is None or text == "":
            question = QMessageBox.question(self, "没有运行路径", "是否选择路径?")
            if question == QMessageBox.StandardButton.Yes:
                self._edit_text()
            else:
                print("自己手动进入选择")
        else:
            try:
                print("执行中")
                self.run_shell(text)
            except FileNotFoundError as ex:
                QErrorMessage(self).showMessage("没有找到路径错误" + text)
            except FileExistsError as ex:
                QErrorMessage(self).showMessage("路径错误" + text)
            except Exception as ex:
                QErrorMessage(self).showMessage("其他错误" + str(ex))
        pass

    # 双击输入框监听
    def eventFilter(self, widget, event):
        if widget == self._url_path_txt:
            if event.type() == QEvent.Type.MouseButtonDblClick:
                self._edit_text()
                pass
            # elif event.type() == QEvent.Type.FocusIn:
            #     self.clicked.emit()   #当焦点再次落到edit输入框时，发送clicked信号出去
            else:
                pass
        return False


# git 自动控件
class AutoGitPush(BaseLineWidget):
    def __init__(self):
        super(AutoGitPush, self).__init__("git自动上传", "请输入需要处理的git地址", SelectFileType.Dir)

    def run_shell(self, path):
        uploadAllFileToGithub.AutoUpGit(path).run()


# 视频转m3u8
class VideoToM3U8(BaseLineWidget):
    def __init__(self):
        super(VideoToM3U8, self).__init__("视频转m3u8", "请输入需要处理的视频地址", SelectFileType.VideoFile)
        pass

    def run_shell(self, path):
        print("执行中")
        print("当前环境" + os.getcwd())
        cwd_path = os.path.dirname(os.path.abspath(__file__))
        if cwd_path != os.getcwd():
            print("设置当前环境" + cwd_path)
            os.chdir(cwd_path)
        print("开始转换视频：" + path)

        worker = WorkerShellRun(["./video_2_m3u8.sh", path])
        self._thread_pool.start(worker)


# 加密mp4视频
class EncodeMp4Video(BaseLineWidget):
    def __init__(self):
        super(EncodeMp4Video, self).__init__("加密mp4视频", "请输入需要处理的视频地址", SelectFileType.VideoFile)
        pass

    def run_shell(self, path):
        print("执行中")
        print("当前环境" + os.getcwd())
        cwd_path = os.path.dirname(os.path.abspath(__file__))
        if cwd_path != os.getcwd():
            print("设置当前环境" + cwd_path)
            os.chdir(cwd_path)
        print("开始转换视频：" + path)

        worker = WorkerShellRun(["./encode.sh", path])
        self._thread_pool.start(worker)


# 解密mp4视频
class DecodeMp4Video(BaseLineWidget):
    def __init__(self):
        super(DecodeMp4Video, self).__init__("解密mp4视频", "请输入需要处理的视频地址", SelectFileType.VideoFile)
        pass

    def run_shell(self, path):
        print("执行中")
        print("当前环境" + os.getcwd())
        cwd_path = os.path.dirname(os.path.abspath(__file__))
        if cwd_path != os.getcwd():
            print("设置当前环境" + cwd_path)
            os.chdir(cwd_path)
        print("开始转换视频：" + path)

        worker = WorkerShellRun(["./DencryVideo.sh", path])
        self._thread_pool.start(worker)


# 解密mp4视频 可以播放加密视频
class PlayMp4Video(BaseLineWidget):
    def __init__(self):
        super(PlayMp4Video, self).__init__("ffmpeg播放mp4视频", "请输入需要处理的视频地址", SelectFileType.VideoFile)
        pass

    def run_shell(self, path):
        print("执行中")
        print("当前环境" + os.getcwd())
        cwd_path = os.path.dirname(os.path.abspath(__file__))
        if cwd_path != os.getcwd():
            print("设置当前环境" + cwd_path)
            os.chdir(cwd_path)
        print("开始转换视频：" + path)

        worker = WorkerShellRun(["./playEncryVideo.sh", path])
        self._thread_pool.start(worker)


# 软连接路径
class MacLnAndroid(BaseLineWidget):
    __suffix_apk = ".apk"

    def __init__(self):
        super(MacLnAndroid, self).__init__("软连接反编译Apk", "请输入反编译文件路径", SelectFileType.ApkFile)

    def run_shell(self, path):
        AndroidComToSmaliAs(path).run()
        print("软连接", path, "成功")


class ApkDecompilation(BaseLineWidget):
    def __init__(self):
        super(ApkDecompilation, self).__init__("生成Apk反编译工程 会卡UI线程", "请输入反编译文件路径", SelectFileType.ApkFile)
        self.android_tools_path = "AndroidTools"
        self.apktool = os.path.join(self.android_tools_path, "apktool_2.7.0.jar")
        self.apktool_url = "https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.7.0.jar"
        self.jadx_path = os.path.join(self.android_tools_path, "jadx-1.4.7/bin/jadx")
        self.jadx_url = "https://github.com/skylot/jadx/releases/download/v1.4.7/jadx-1.4.7.zip"

    def run_shell(self, path):
        # if not os.path.exists(self.android_tools_path):
        #     os.mkdir(self.android_tools_path)
        # if not os.path.exists(self.apktool):
        #     dw = DownloadWidget(self.apktool_url, self.apktool)
        #     dw.run()
        # if not os.path.exists(self.jadx_path):
        #     dw = DownloadWidget(self.jadx_url, self.android_tools_path)
        #     dw.run()
        #     zw = ZipWidget(dw.file)
        #     zw.run()
        # 
        # apk_name = os.path.splitext(path)[0]
        # # 使用apktool导出反编译工程
        # shell = ShellWidget()
        # apk_tools_dir_path = os.path.join(os.path.dirname(path), apk_name)  # apk 反编译工程路径
        # shell.run(["java", "-jar", self.apktool, "d", "-o", apk_tools_dir_path, path])
        # 
        # # 虽然不会失去相应 但是这是一个新的线程 所以无法准切的知道执行完成否 如果使用
        # # cmd = ["java", "-jar", self.apktool, "d", "-o",
        # #        os.path.join(os.path.dirname(path), os.path.basename(path).split(".")[0]),
        # #        path]
        # # worker = WorkerShellRun(cmd)
        # # self._thread_pool.start(worker)
        # 
        # # 使用jadx导出Androidstudio工程 方便阅读代码
        # as_path = os.path.join(os.path.dirname(path), apk_name + "_android_studio")  # 反编译AndroidStudio工程路径
        # 
        # shell = ShellWidget()
        # shell.run([self.jadx_path, "-e", "-d", as_path, path])
        # 
        # # 连接反编译工程的 smali 到AndroidStudio 的smails中
        # as_smali_path = os.path.join(as_path, "app/src/main/smalis")
        # if not os.path.exists(as_smali_path):
        #     os.mkdir(as_smali_path)
        # smali_path = []
        # for _path in os.listdir(apk_tools_dir_path):
        #     if "smali" in _path:
        #         smali_path.append(_path)
        # for smali in smali_path:
        #     _smali_path = os.path.join(apk_tools_dir_path, smali)
        #     cmd = ["ln", "-s", _smali_path,
        #            as_smali_path]  # 软连接源路径一定得是绝对路径
        #     worker = WorkerShellRun(cmd)
        #     self._thread_pool.start(worker)

        ApkTool(path).run()
        JadxTool(path).run()
        AndroidComToSmaliAs(path).run()
        print("生成反编译{}工程成功".format(path))


def main():
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    ex = MainWindow()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

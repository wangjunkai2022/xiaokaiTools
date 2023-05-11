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
        super(MacLnAndroid, self).__init__("软连接反编译Android smali到Android路径下", "请输入反编译文件夹路径", SelectFileType.Dir)
        self._input_path = ""

    def cmd_callback(self):
        self.run_shell(self._input_path)

    def run_shell(self, path):
        self._input_path = path
        print("软连接路径")
        # 查找文件夹下的原版Apk包
        os.chdir(path)  # 设置工作路径为 输入的路径
        apks = []
        for dataname in os.listdir("./"):
            if os.path.splitext(dataname)[1] == self.__suffix_apk:  # 目录下包含.apk的文件
                # print(dataname)
                apks.append(dataname)

        for name in apks:
            path = name[0:len(name) - len(self.__suffix_apk)]
            android_studio_path = "android_studio"
            if not os.path.exists(android_studio_path):
                question = QMessageBox.question(self, "没有对应的Android工程", "是否生成Android工程\n生成安卓工程前需要选择jadx")
                if question == QMessageBox.StandardButton.Yes:
                    jadx_path, ok = QFileDialog.getOpenFileName(self)
                    if ok and "jadx" in jadx_path:
                        cmd = [
                            jadx_path, "-d", "./android_studio", "--export-gradle", name
                        ]
                        worker = WorkerShellRun(cmd)
                        worker.set_callback(self.cmd_callback)
                        self._thread_pool.start(worker)
                        print("生成Android工程中。。。。请等待结束 再次生成软连接")
                    else:
                        print("选择的jadx不对")
                else:
                    print("自己手动用jadx生成")
                print("生成软连接失败")
                return
            android_smali_path = os.path.join(android_studio_path, "app/src/main/smalis")
            if not os.path.exists(android_smali_path):
                os.mkdir(android_smali_path)
            if os.path.exists(path):  # 反编译路径是否存在
                smali_path = []
                for _path in os.listdir(path):
                    if "smali" in _path:
                        smali_path.append(_path)
                for smali in smali_path:
                    _smali_path = os.path.join(path, smali)
                    cmd = ["ln", "-s", os.path.abspath("./" + _smali_path),
                           "./" + android_smali_path]  # 软连接源路径一定得是绝对路径
                    worker = WorkerShellRun(cmd)
                    self._thread_pool.start(worker)
                print("软连接", name, "成功")



def main():
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    ex = MainWindow()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

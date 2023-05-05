# !/usr/bin/python3
import os
import subprocess
import tempfile
import time

import sh as sh
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

        self.process = QTextEdit(self, readOnly=True)
        self.process.ensureCursorVisible()
        self._clean_debug_btn = QPushButton("清除记录")
        self._clean_debug_btn.clicked.connect(lambda: self.process.setText(""))
        self._mainQVLayout.addWidget(self._clean_debug_btn)
        self._mainQVLayout.addWidget(self.process)

        self.setGeometry(300, 300, 450, 350)
        self.setWindowTitle('PyQt6_Tool_Windows')
        self.show()


# git 自动控件
class AutoGitPush(QWidget):
    def __init__(self):
        super(AutoGitPush, self).__init__()
        # self.parent = parent
        self.horizontal_layout = QHBoxLayout()
        self._run_btn = QPushButton('开始')
        self.horizontal_layout.addWidget(QLabel("git自动上传"))
        self.horizontal_layout.addWidget(self._run_btn)
        self.setLayout(self.horizontal_layout)
        self._run_btn.clicked.connect(self._runBtn)

        # 输入框
        self._url_path_txt = QLineEdit()
        self.horizontal_layout.addWidget(self._url_path_txt)
        self._url_path_txt.setPlaceholderText("请输入需要处理的git地址")
        self._url_path_txt.installEventFilter(self)
        # self._url_path_txt.mouseDoubleClickEvent(self)

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

    def _runBtn(self):
        text = self._url_path_txt.text()
        if text is None or text == "":
            self._edit_text()
            self._runBtn()
        else:
            try:
                print("执行中")
                uploadAllFileToGithub.AutoUpGit(text).run()
            except FileNotFoundError as ex:
                QErrorMessage(self).showMessage("没有找到路径错误" + text)
            except FileExistsError as ex:
                QErrorMessage(self).showMessage("路径错误" + text)
            except Exception as ex:
                QErrorMessage(self).showMessage("其他错误" + str(ex))
            print("执行完毕")

    def _edit_text(self):
        txt = self._url_path_txt.text()
        if txt is None or txt == "":
            dir = QFileDialog.getExistingDirectory(self, "选择文件夹", "/")
            self._url_path_txt.setText(dir)
        else:
            pass


# 开启新线程执行cmd命令
class WorkerShellRun(QRunnable):
    def __init__(self, cmd):
        super(WorkerShellRun, self).__init__()
        self.cmd = cmd
        self._init()

    def _init(self):
        evn = os.environ.copy()
        evn["PATH"] = evn["PATH"] + ":/usr/local/bin"
        self.popen = subprocess.Popen(self.cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT, text=True, env=evn)

    def run(self):
        while True:
            # time.sleep(0.5)
            out = self.popen.stdout.readline()
            if out != "":
                print(out)
            if out == '' and self.popen.poll() != None:
                print("执行完毕")
                return


class VideoToM3U8(QWidget):
    def __init__(self):
        super(VideoToM3U8, self).__init__()
        self.horizontal_layout = QHBoxLayout()
        self._run_btn = QPushButton('开始')
        self.horizontal_layout.addWidget(QLabel("视频转m3u8"))
        self.horizontal_layout.addWidget(self._run_btn)
        self.setLayout(self.horizontal_layout)
        self._run_btn.clicked.connect(self._runBtn)

        # 输入框
        self._url_path_txt = QLineEdit()
        self.horizontal_layout.addWidget(self._url_path_txt)
        self._url_path_txt.setPlaceholderText("请输入需要处理的视频地址")
        self._url_path_txt.installEventFilter(self)

        self._thread_pool = QThreadPool()
        pass

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

    def _runBtn(self):
        text = self._url_path_txt.text()
        if text is None or text == "":
            self._edit_text()
            self._runBtn()
        else:
            try:
                print("执行中")
                print("当前环境" + os.getcwd())
                path = os.path.dirname(os.path.abspath(__file__))
                if path != os.getcwd():
                    print("设置当前环境" + path)
                    os.chdir(path)
                print("开始转换视频：" + text)

                worker = WorkerShellRun(["./video_2_m3u8.sh", text])
                self._thread_pool.start(worker)
            except FileNotFoundError as ex:
                QErrorMessage(self).showMessage("没有找到路径错误" + text)
            except FileExistsError as ex:
                QErrorMessage(self).showMessage("路径错误" + text)
            except Exception as ex:
                QErrorMessage(self).showMessage("其他错误" + str(ex))
            # print("执行完毕")

    def _edit_text(self):
        txt = self._url_path_txt.text()
        if txt is None or txt == "":
            dir, ok = QFileDialog.getOpenFileName(self) or ""
            if ok:
                self._url_path_txt.setText(dir)
        else:
            pass


class Stream(QObject):
    """Redirects console output to text widget."""
    newText = pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))


def main():
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    ex = MainWindow()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

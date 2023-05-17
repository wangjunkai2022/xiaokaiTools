import os
import zipfile

import requests
from PyQt6.QtCore import QProcess, Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtWidgets import QWidget, QProgressDialog, QMessageBox


# 运行shell 有卡UI线程 假死的bug
class ShellWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.handle_output)
        self.process.readyReadStandardError.connect(self.handle_error)
        self.process.finished.connect(self.handle_finish)
        # self.isRuning = True

    def handle_error(self):
        error = self.process.readAllStandardError().data().decode("utf-8").strip()
        print(error)

    def handle_output(self):
        output = self.process.readAllStandardOutput().data().decode("utf-8").strip()
        print(output)

    # Do something with the output
    def handle_finish(self):
        # self.button.setEnabled(True)
        self.process.close()
        print("执行完毕")

    def run(self, cmd):
        if isinstance(cmd, list):
            _cmd = cmd[0]
            args = []
            for code in cmd:
                if code != _cmd:
                    args.append(code)
            # _cmd = ""
            # for code in cmd:
            #     _cmd += code + " "
            self.process.start(_cmd, args)
        elif isinstance(cmd, str):
            self.process.start(cmd)
        self.process.waitForFinished()


# 执行下载
class DownloadWidget(QWidget):
    def __init__(self, url, file=None):
        super().__init__()
        self.url = url
        self.is_exists = False
        if file is None:
            self.file = "./" + os.path.basename(url)
        elif os.path.isdir(file):
            if not os.path.exists(file):
                os.mkdir(file)
            self.file = os.path.join(file, os.path.basename(url))
            self.is_exists = os.path.exists(self.file)
        else:
            self.file = file

    def run(self):
        if self.is_exists:
            print("文件存在 没有下载")
            question = QMessageBox.question(self, "文件存在", "是否重新下载？")
            if question == QMessageBox.StandardButton.Yes:
                os.remove(self.file)
            else:
                return

        response = requests.get(self.url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        progress_dialog = QProgressDialog("文件{}下载中".format(self.file), '取消下载', 0, total_size, self)
        progress_dialog.setWindowTitle('下载中')
        progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        progress_dialog.show()

        data = b''
        for data_chunk in response.iter_content(block_size):
            data += data_chunk
            progress_dialog.setValue(len(data))
            if progress_dialog.wasCanceled():
                response.close()
                break

        with open(self.file, 'wb') as f:
            f.write(data)


# 解压文件到指定目录
# class ZipToWidget(QWidget):
#     def __init__(self, file: str, path):
#         super(ZipToWidget, self).__init__()
#         if path is None or path == "" or path == " ":
#             self.path = file.split(".")
#         else:
#             self.path = path
#         if file.endswith(".zip"):
#             self.file = file
# 
#     def run(self):
#         zipfile.ZipFile(self.file).extractall(self.path)

# 解压zip文件到指定目录
class ZipWidget(QWidget):
    # 如果path为空时会在当前zip文件下新建一个zip文件名的文件夹并解压到此文件夹下
    def __init__(self, file: str, path=None):
        super().__init__()
        if file.endswith(".zip"):
            self.src_path = file
        if path is None or path == "" or path == " ":

            name = os.path.splitext(self.src_path)[0]  # 获取不含后缀的文件名
            # name = name.split('.')[-1]
            self.dst_path = name
        else:
            self.dst_path = path

    def run(self):
        zipfile_file = zipfile.ZipFile(self.src_path, 'a')
        progress_dialog = QProgressDialog("文件{}解压中".format(self.src_path), '取消下载', 0,
                                          len(zipfile_file.infolist()), self)
        progress_dialog.setWindowTitle('下载中')
        progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        progress_dialog.show()
        with zipfile_file as z:
            # total_size = sum((file.file_size for file in z.infolist()))
            # extracted_size = 0
            index = 0
            for file in z.infolist():
                # extracted_size += file.file_size
                progress = index
                progress_dialog.setValue(progress)
                z.extract(file, self.dst_path)
                os.chmod(os.path.join(self.dst_path, file.filename), 0o755)  # 给予运行权限
                index += 1

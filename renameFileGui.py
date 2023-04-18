import sys
import os
import shutil
from PIL import Image
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QFileDialog
from PyQt5 import QtWidgets, QtGui


class RenameFile(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 标签
        self.input_label = QLabel('', self)
        self.input_label.move(20, 25)

        # 输入框
        self.input_text = QLineEdit(self)
        self.input_text.move(100, 20)
        self.input_text.resize(200, 25)
        self.input_text.setEnabled(False)

        self.button = QPushButton('浏览', self)  # 创建选择文件夹按钮
        self.button.move(310, 21)
        self.button.clicked.connect(self.showDialog)  # 将单击按钮的事件连接到 showDialog 方法

        # 执行按钮
        self.run_button = QPushButton('执行', self)
        self.run_button.move(310, 65)
        # 信号连接
        self.run_button.pressed.connect(self.run_script)
        self.run_button_hide()

        self.input_label = QLabel('请使用前备份源文件数据,如有异常，开发者不负任何责任！', self)
        self.input_label.move(20, 120)
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(10)  # 括号里的数字可以设置成自己想要的字体大小
        font.setFamily("SimHei")  # 宋体
        self.input_label.setFont(font)

        # 显示结果
        self.result_label = QLabel('', self)
        self.result_label.resize(200, 20)
        self.result_label.move(20, 70)

        # 日志控件
        self.log_text = QtWidgets.QTextEdit()
        self.log_text.setReadOnly(True)

        # 布局控件
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.input_label)
        layout.addWidget(self.result_label)

        layout.addWidget(self.input_text)

        layout.addWidget(self.button)

        layout.addWidget(self.run_button)
        layout.addWidget(self.log_text)

        # 界面设置
        self.setGeometry(300, 300, 420, 300)
        self.setWindowTitle('文件批量重命名并将图片转为JPG格式（名称排名后重命名为三位自增数字序列）')
        self.show()

    def showDialog(self):
        folderName = QFileDialog.getExistingDirectory(self, 'Select Folder')  # 打开文件夹对话框，选择文件夹
        if folderName:
            self.input_text.setText(folderName)
            print(f'Selected folder: {folderName}')
        self.run_button_show()

    def run_script(self):
        # 开始输出日志
        self.log('开始执行...')
        # 获取输入参数
        self.run_button_hide()
        arg = self.input_text.text()
        try:
            # 执行脚本
            result = self.convert_image_and_rename_file(arg)
            # 显示结果
            self.result_label.setText(result)
            self.result_label.setText('执行完成')
            self.log('执行结束...')
        except Exception as e:
            # 出现异常输出日志
            self.log('出现异常：%s' % str(e))
            # 结束输出日志

    def run_button_hide(self):
        self.run_button.setEnabled(False)

    def run_button_show(self):
        self.run_button.setEnabled(True)

    def log(self, msg):
        self.log_text.append(msg)
        # 滚动到最底部
        cursor = self.log_text.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        self.log_text.setTextCursor(cursor)
        self.log_text.ensureCursorVisible()

    # 处理文件并且重命名文件
    def convert_image_and_rename_file(self, path):
        new_path = self.copy_path(path)
        self.convert_image_to_jpg(new_path)
        self.rename(new_path)
        return "成功"

    # 复制文件夹
    def copy_path(self, path):
        # 获取当前文件夹的绝对路径和文件夹名称
        dir_path = os.path.abspath(path)
        dir_name = os.path.basename(dir_path)
        # 获取当前文件夹的上一级目录的绝对路径
        parent_path = os.path.dirname(dir_path)
        # 在上一级目录下创建同样的文件夹
        new_dir_path = os.path.join(parent_path, dir_name + '_copy')
        if os.path.exists(new_dir_path):
            shutil.rmtree(new_dir_path)
        os.mkdir(new_dir_path)
        # 遍历原始文件夹中的所有文件和文件夹，并将它们复制到副本文件夹中
        for item in os.listdir(path):
            source_item_path = os.path.join(path, item)
            destination_item_path = os.path.join(new_dir_path, item)
            if os.path.isfile(source_item_path):
                self.log("复制中.......")
                shutil.copy2(source_item_path, destination_item_path)
            else:
                self.log("复制中.......")
                shutil.copytree(source_item_path, destination_item_path)
        self.log(f"{new_dir_path} 文件夹已创建并复制完毕。")
        print(f"{new_dir_path} 文件夹已创建并复制完毕。")
        return new_dir_path

    # 文件格式转换为jpg
    def convert_image_to_jpg(self, path):
        # 遍历指定文件夹下的所有图片文件
        for root, dirs, files in os.walk(path):
            for name in files:
                # 获取图片文件的路径
                img_path = os.path.join(root, name)
                # 打开图片文件
                img = Image.open(img_path)
                # 如果当前图片格式不是jpg，则进行转换，否则跳过
                if img.format != 'JPEG':
                    # 获取图片保存的路径
                    path, ext = os.path.splitext(img_path)
                    new_path = path + '.jpg'
                    # 将图片保存为jpg格式
                    img = img.convert('RGB')
                    os.remove(img_path)
                    img.save(new_path, format='JPEG')
                    print('将%s转换为jpg格式并保存为%s' % (name, new_path))
                    self.log('将%s转换为jpg格式并保存为%s' % (name, new_path))
                else:
                    print('%s已经是jpg格式，不需要进行转换' % name)
                    self.log('%s已经是jpg格式，不需要进行转换' % name)

    # 重命名文件
    def rename(self, path):
        # 遍历指定文件夹下的所有图片文件
        for root, dirs, files in os.walk(path):
            i = 1
            files.sort()  # 按名称排序
            for file in files:
                # 获取文件后缀
                suffix = os.path.splitext(file)[1]
                # 构建新的文件名
                new_name = '{:03d}{}'.format(i, suffix)
                i += 1
                # 重命名文件
                os.rename(os.path.join(root, file), os.path.join(root, new_name))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_app = RenameFile()
    sys.exit(app.exec_())



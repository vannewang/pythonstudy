import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QFileDialog
from renamefile import convert_image_and_rename_file


class RenameFile(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 标签
        self.input_label = QLabel('文件夹路径:', self)
        self.input_label.move(20, 25)

        # # 输入框
        self.input_text = QLineEdit(self)
        self.input_text.move(100, 20)
        self.input_text.resize(200, 25)
        # self.input_text

        self.button = QPushButton('浏览', self)  # 创建选择文件夹按钮
        self.button.move(310, 21)
        self.button.clicked.connect(self.showDialog)  # 将单击按钮的事件连接到 showDialog 方法

        self.setGeometry(300, 300, 250, 150)

        # 执行按钮
        self.run_button = QPushButton('执行', self)
        self.run_button.move(310, 65)
        # self.run_button.resize(80, 40)
        # 信号连接
        self.run_button.clicked.connect(self.run_script)

        self.input_label = QLabel('请使用前备份源文件数据,如有异常，开发者不负任何责任！', self)
        self.input_label.move(20, 120)

        # 显示结果
        self.result_label = QLabel('', self)
        self.result_label.move(20, 70)
        self.resize(200, 200)

        # 界面设置
        self.setGeometry(300, 300, 400, 150)
        self.setWindowTitle('文件批量重命名并将图片转为JPG格式（名称排名后重命名为三位自增数字序列）')
        self.show()

    def showDialog(self):
        folderName = QFileDialog.getExistingDirectory(self, 'Select Folder')  # 打开文件夹对话框，选择文件夹
        if folderName:
            self.input_text.setText(folderName)
            print(f'Selected folder: {folderName}')

    def run_script(self):
        # 获取输入参数
        arg = self.input_text.text()
        # 执行脚本
        result = convert_image_and_rename_file(arg)
        # 显示结果
        self.result_label.setText(result)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_app = RenameFile()
    sys.exit(app.exec_())

import os
from typing import List

import exifread
from PyQt5.QtWidgets import QFileDialog, QWidget, QPushButton, QApplication, QTableWidget, QVBoxLayout, QHBoxLayout, \
    QTableWidgetItem


class AppendDatetime:
    paths_list: List[str] = list()

    def __init__(self, paths_list: List[str] = None):
        if paths_list is not None:
            for file_path in paths_list:
                if os.path.isfile(file_path) and (file_path not in self.paths_list):
                    self.paths_list.append(file_path)

    # 添加文件
    def append(self, paths_list: List[str]):
        for file_path in paths_list:
            if os.path.isfile(file_path) and (file_path not in self.paths_list):
                self.paths_list.append(file_path)

    # 清空文件
    def clear_paths_list(self):
        self.paths_list = list()

    # 获得当前的所有文件路径列表
    def get_paths_list(self) -> List[str]:
        return self.paths_list

    # 判断各个文件是否包含exif信息
    def is_contains_exif(self) -> List[bool]:
        ans = list()
        for file_path in self.paths_list:
            FIELD = 'EXIF DateTimeOriginal'
            fd = open(file_path, 'rb')
            tags = exifread.process_file(fd)
            fd.close()
            if FIELD in tags:
                ans.append(True)
            else:
                ans.append(False)
        return ans

    # 获得新名
    def get_new_names(self) -> List[str]:
        new_names = list()

        # 执行重命名
        def process(filename):
            FIELD = 'EXIF DateTimeOriginal'
            fd = open(filename, 'rb')
            tags = exifread.process_file(fd)
            fd.close()
            if FIELD in tags:
                new_name = str(tags[FIELD]).replace(' ', '_').replace(':', '') + os.path.splitext(filename)[1]
                #        print(tags[FIELD])

                date, time = str(tags[FIELD]).split(' ')
                date = date.split(':')[1] + '月' + date.split(':')[-1] + '日'
                time = time.split(':')[0] + '时' + time.split(':')[1] + '分'
                date_time = date + '_' + time
                #        print(date_time)
                #        print(filename)
                new_name = os.path.splitext(filename)[0] + '_' + date_time + os.path.splitext(filename)[1]

                tot = 1
                while os.path.exists(new_name):
                    new_name = os.path.splitext(filename)[0] + '_' + date_time + '_' + str(tot) + \
                               os.path.splitext(filename)[1]
                    tot += 1

                print(new_name)
                new_names.append(new_name)
                # os.rename(filename, new_name)
            else:
                new_names.append('')
                print('No {} found'.format(FIELD))

        for file_path in self.paths_list:
            process(file_path)
        return new_names

    # 重命名
    def rename(self):
        if self.paths_list:
            for old_name, new_name in zip(self.paths_list, self.get_new_names()):
                if new_name:
                    os.rename(old_name, new_name)


class MyWindow(QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.append_datetime = AppendDatetime()
        self.setGeometry(100, 100, 1000, 800)
        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        btn_widget = QWidget()

        self.get_files_btn = QPushButton('添加文件')
        self.get_files_btn.setObjectName("get files names")
        self.get_files_btn.clicked.connect(self.msg)

        clear_table_btn = QPushButton('不重命名，清空列表')
        clear_table_btn.clicked.connect(self.clear_table)

        h_layout.addWidget(self.get_files_btn)
        h_layout.addWidget(clear_table_btn)
        btn_widget.setLayout(h_layout)

        self.clear_paths_btn = QPushButton('清空列表')
        self.clear_paths_btn.clicked.connect(self.clear_table)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['原名', '新文件名预览', '是否包含EXIF信息'])
        self.table.setColumnWidth(0, 300)
        self.table.setColumnWidth(1, 500)
        self.table.setColumnWidth(2, 100)

        rename_btn = QPushButton('执行重命名')
        rename_btn.clicked.connect(self.on_clicked_rename)

        v_layout.addWidget(btn_widget)
        v_layout.addWidget(self.table)
        v_layout.addWidget(rename_btn)

        self.setLayout(v_layout)

    def msg(self):
        files, ok1 = QFileDialog.getOpenFileNames(self, "多文件选择", "/", "Photo Files (*)")
        # print(files, ok1)
        self.append_datetime.append(files)
        self.update_table()

    def update_table(self):
        self.table.setRowCount(0)
        for row, [path, new_name, has_exif] in enumerate(
                zip(self.append_datetime.get_paths_list(),
                    self.append_datetime.get_new_names(),
                    self.append_datetime.is_contains_exif()
                    )):
            self.table.setRowCount(self.table.rowCount() + 1)
            self.table.setItem(row, 0, QTableWidgetItem(path))
            self.table.setItem(row, 1, QTableWidgetItem(new_name))
            self.table.setItem(row, 2, QTableWidgetItem('是' if has_exif else '否'))

    def clear_table(self):
        self.append_datetime.clear_paths_list()
        self.table.setRowCount(0)

    def on_clicked_rename(self):
        self.append_datetime.rename()
        self.clear_table()


def main():
    import sys

    app = QApplication(sys.argv)
    w = MyWindow()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

from PyQt5.QtWidgets import QFileDialog, QWidget, QPushButton, QApplication, QTableWidget, QVBoxLayout, QHBoxLayout, \
    QTableWidgetItem
from AppendDatetime import AppendDatetime


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

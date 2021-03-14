import os
import exifread
from typing import List


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


if __name__ == '__main__':
    ls = ['/Users/zcli/Desktop/测试.c.a.txt/IMG_0250.jpeg', '/Users/zcli/Desktop/测试.c.a.txt/IMG_0251.jpeg']
    append_datetime = AppendDatetime(paths_list=ls)
    append_datetime.rename()

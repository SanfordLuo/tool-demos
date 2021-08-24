"""
检测指定目录下所有py文件中是否存在关键字word, 返回关键字所在的py文件
"""
import os

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_PATH = "{}/test".format(PROJECT_PATH)
WORD = "jay"


def get_word_path(dirPath, word):
    status = False
    path_list = []
    for root, dirs, files in os.walk(dirPath):
        for file in files:
            if os.path.splitext(file)[1] == '.py':
                file_path = os.path.join(root, file)
                path_list.append(file_path)

    for file in path_list:
        f = open(file, 'r', encoding="utf-8")
        if word in f.read():
            print("%s关键字在文件%s" % (word, file))
            status = True
        f.close()

    if not status:
        print("%s关键字不存在" % word)


if __name__ == '__main__':
    get_word_path(DIR_PATH, WORD)

#!python3
#encoding:utf-8
import pathlib
import shutil

# ツールがあるが大げさ
# https://github.com/simonwhitaker/gibo
# https://github.com/github/gitignore
# C言語用のは便利そうだが、Pythonは不便そう。
class GitIgnoreFile:
    def __init__(self, args):
        self.__args = args
        self.__path_dir_root = pathlib.Path(__file__).resolve().expanduser().parent.parent
        self.__filename = '.gitignore'

    def Write(self):
        path_tpl = pathlib.Path(self.__path_dir_root / 'res/template/gitignore/.gitignore')
        path_target = pathlib.Path(self.__args.output_dir) / self.__filename
        if path_tpl.is_file() and not path_target.exists():
            shutil.copy(str(path_tpl), str(path_target))

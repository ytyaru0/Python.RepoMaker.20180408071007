#!python3
#encoding:utf-8
import os.path, pathlib
import argparse
import configparser
import sqlite3
import datetime
from TemplateRenderer import TemplateRenderer
from UseLibLicense import UseLibLicense

# https://github.com/simonwhitaker/gibo
# https://github.com/github/gitignore
class GitIgnoreFile:
    def __init__(self, args):
        self.__args = args
        self.__config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        self.__path_dir_root = pathlib.Path(__file__).resolve().expanduser().parent.parent
        self.__path_file_config = None
        self.__filename = 'ReadMe.md'

    def __LoadConfig(self):
        for f in [self.__path_dir_root / 'res/repo.ini']:
            print(f)
            if os.path.isfile(f):
                self.__path_file_config = f
                self.__config.read(str(f))
                return
        raise Exception('repo.iniファイルが存在しません。')

    def Write(self):
        path = pathlib.Path(self.__args.output_dir)
        for ext in ['', '.md', '.txt', '.MD', '.TXT']:
            for filepath in path.glob('*' + ext):
                if not filepath.is_file(): continue
                if 'ReadMe'.lower() == filepath.name.split('.')[0].lower():
                    print('ReadMeファイルが既存のため作成は中止します。: {}'.format(filepath))
                    return
        """
        path = os.path.join(self.__args.output_dir, self.__filename)
        if os.path.isfile(path):
            print('ReadMe.mdが既存のため作成は中止します。')
            return
        """
        self.__LoadConfig()
        tpl_var_dict = {}
        tpl_var_dict['Description'] = self.__args.description
        tpl_var_dict['Environment'] = self.__GetEnvironmentText()
        tpl_var_dict['License'] = self.__GetLicenseText()
        tpl_var_dict['UseLibLicense'] = self.__GetUseLibLicenseText()
        path_tpl = os.path.join(pathlib.Path(__file__).parent.parent / ('res/template/' + self.__filename))
        source = None
        with open(path_tpl) as f: source = f.read()
        res = TemplateRenderer().Render(source, **tpl_var_dict)
        
        path_out = os.path.join(self.__args.output_dir, self.__filename)
        with open(path_out, 'w') as f: f.write(res)
       
    def __GetLicenseText(self):
        path = pathlib.Path(__file__).parent.parent / ('res/template/license/' + self.__args.license)
        if path.is_file():
            source = None
            with path.open() as f: return f.read()
        else:
            try: author = self.__LoadLicenseAuthor()
            except: author = None
            if author is None: author = self.__args.username
            copyright = ''
            if author is not None: copyright = '\n\n' + 'Copyright (c) {} {}'.format('{0:%Y}'.format(datetime.datetime.now()), author)
            return 'このソフトウェアは[{}](LICENSE.txt)ライセンスである。'.format(self.__args.license) + copyright

    def __GetEnvironmentText(self):
        ext = self.__GetExtension()
        if ext is None: return ''
        path = pathlib.Path(__file__).parent.parent / ('res/template/env/' + self.__GetOsName() + '_' + ext + '.md')
        if path.is_file():
            source = None
            with path.open() as f: return f.read().strip()
            
    def __GetOsName(self):
        return self.__config['Environment']['OsAbbr']
    def __GetExtension(self):
        # A. プロジェクト名から取得する
        lang = os.path.dirname(self.__args.output_dir).split('.')[0]
        import csv
        with open(os.path.expanduser('~/root/db/programming/languages.tsv')) as f:
            tsv = csv.reader(f, delimiter='\t')
            for r in tsv:
                if lang.lower() == r[0].lower():
                    return r[1]
        # B. self.__args.extension
        if self.__args.extension is not None and isinstance(self.__args.extension,(list,tuple)): return self.__args.extension[0]
        else: return None

    def __GetUseLibLicenseText(self):
        return UseLibLicense(self.__args).GetMarkdownTable()

    def __RaiseLoadLicenseDbPath(self):
        if 'Db' not in self.__config.sections(): raise Exception('Dbセクションがありません。file={}'.format(self.__path_file_config))
        if 'Licenses' not in self.__config['Db']: raise Exception('DbセクションにLicensesキーがありません。LicensesDBファイルパスを指定してください。file={}'.format(self.__path_file_config))
        if '' ==  self.__config['Db']['Licenses'].strip(): raise Exception('DbセクションのLicensesキーに値がありません。LicensesDBファイルパスを指定してください。file={}'.format(self.__path_file_config))
        return pathlib.Path(self.__config['Db']['Licenses']).expanduser().resolve()
  
    def __LoadLicenseAuthor(self):
        if 'License' not in self.__config.sections(): raise Exception('Licenseセクションがありません。file={}'.format(self.__path_file_config))
        if 'Author' not in self.__config['License']: raise Exception('LicenseセクションにAuthorキーがありません。著者名を入力してください。file={}'.format(self.__path_file_config))
        if '' ==  self.__config['License']['Author'].strip(): raise Exception('LicenseセクションのAuthorキーに値がありません。著者名を入力してください。file={}'.format(self.__path_file_config))
        return self.__config['License']['Author']

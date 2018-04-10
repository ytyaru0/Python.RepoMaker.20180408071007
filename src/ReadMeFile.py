#!python3
#encoding:utf-8
import os.path, pathlib
import argparse
import configparser
import sqlite3
import datetime
from TemplateRenderer import TemplateRenderer
from UseLibLicense import UseLibLicense

class ReadMeFile:
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
        path = os.path.join(self.__args.output_dir, self.__filename)
        if os.path.isfile(path):
            print('ReadMe.mdが既存のため作成は中止します。')
            return
        
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
        
        """
        licenseDbPath = self.__RaiseLoadLicenseDbPath()
        record = self.__SelectLicense(licenseDbPath )
        if record is None: raise Exception("指定されたライセンス'{}'はDBに存在しません。DBに存在するライセンスは次のとおりです。{}".format(self.__args.license, self.__SelectAllKeys(licenseDbPath )))
        
        source = self.__Replace(record[0])
        with open(path, 'w') as f: f.write(source)
        """
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
        #return ''

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

    """
    def __SelectLicense(self, licenseDbPath):
        conn = sqlite3.connect(str(licenseDbPath))
        cur = conn.cursor()
        cur.execute("select Body from Licenses where Key='{}';".format(self.__args.license))
        res = cur.fetchone()
        conn.close()
        return res

    def __SelectAllKeys(self, licenseDbPath):
        conn = sqlite3.connect(str(licenseDbPath))
        cur = conn.cursor()
        cur.execute("select Key from Licenses order by Key asc;".format(self.__args.license))
        res = cur.fetchall()
        conn.close()
        #return res
        return [r[0] for r in res if 'other' != r[0]]
    def __Replace(self, source):
        author = None
        try: author = self.__LoadLicenseAuthor()
        except: pass
        if author is None: author = self.__args.username
        if '[fullname]' in source and author is None:
            raise Exception("ライセンス'{}'には著作者名が必要です。起動引数-uか、repo.iniの[License]Authorを指定してください。".format(self.__args.license))
        elif author is not None:
            res = source.replace('[year]', '{0:%Y}'.format(datetime.datetime.now()))
            return res.replace('[fullname]', author)
        else:
            return source.replace('[year]', '{0:%Y}'.format(datetime.datetime.now()))
    """


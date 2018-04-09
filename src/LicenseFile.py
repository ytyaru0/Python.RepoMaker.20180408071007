#!python3
#encoding:utf-8
import os.path, pathlib
import argparse
import configparser
import sqlite3
import datetime

class LicenseFile:
    def __init__(self, args):
        self.__args = args
        #self.__config = configparser.ConfigParser()
        self.__config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        self.__path_dir_root = pathlib.Path(__file__).resolve().expanduser().parent.parent
        self.__path_file_config = None

    def __LoadConfig(self):
        for f in [self.__path_dir_root / 'res/repo.ini']:
            print(f)
            if os.path.isfile(f):
                self.__path_file_config = f
                self.__config.read(str(f))
                return
        raise Exception('repo.iniファイルが存在しません。')

    def Write(self):
        path = os.path.join(self.__args.output_dir, 'LICENSE.txt')
        if os.path.isfile(path):
            print('LICENSE.txtが既存のため作成は中止します。')
            return
        
        self.__LoadConfig()
        licenseDbPath = self.__RaiseLoadLicenseDbPath()
        record = self.__SelectLicense(licenseDbPath )
        if record is None: raise Exception("指定されたライセンス'{}'はDBに存在しません。DBに存在するライセンスは次のとおりです。{}".format(self.__args.license, self.__SelectAllKeys(licenseDbPath )))
        
        with open(path, 'w') as f:
            f.write(self.__Replace(record[0]))
 
    def __RaiseLoadLicenseDbPath(self):
        if 'Db' not in self.__config.sections(): raise Exception('Dbセクションがありません。file={}'.format(self.__path_file_config))
        if 'Licenses' not in self.__config['Db']: raise Exception('DbセクションにLicensesキーがありません。LicensesDBファイルパスを指定してください。file={}'.format(self.__path_file_config))
        if '' ==  self.__config['Db']['Licenses'].strip(): raise Exception('DbセクションのLicensesキーに値がありません。LicensesDBファイルパスを指定してください。file={}'.format(self.__path_file_config))
        return pathlib.Path(self.__config['Db']['Licenses']).expanduser().resolve()

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
 
    def __LoadLicenseAuthor(self):
        if 'License' not in self.__config.sections(): raise Exception('Licenseセクションがありません。file={}'.format(self.__path_file_config))
        if 'Author' not in self.__config['License']: raise Exception('LicenseセクションにAuthorキーがありません。著者名を入力してください。file={}'.format(self.__path_file_config))
        if '' ==  self.__config['License']['Author'].strip(): raise Exception('LicenseセクションのAuthorキーに値がありません。著者名を入力してください。file={}'.format(self.__path_file_config))
        return self.__config['License']['Author']


    def __Replace(self, source):
        author = None
        try: author = self.__LoadLicenseAuthor()
        except: pass
        if author is None: author = self.__args.username
        if '[fullname]' in source and author is None:
            raise Exception("ライセンス'{}'には著作者名が必要です。起動引数-uか、repo.iniの[License]Authorを指定してください。".format(self.__args.license))
        res = source.replace('[year]', '{0:%Y}'.format(datetime.datetime.now()))
        return res.replace('[fullname]', self.__args.username)

#!python3
#encoding:utf-8
import os.path, pathlib
import argparse, configparser
import sqlite3
import datetime
import io
import re
from CopyRightSearcher import CopyRightSearcher

# 使用ライブラリのライセンス情報を取得してmarkdownのテーブル形式として返却する
# ソースコードから解析するのは難易度が高いので、
# 仮想環境下にある全パッケージからライセンス情報を取得する。
# http://tell-k.hatenablog.com/entry/2012/02/04/131805
# https://docs.python.jp/3/distutils/examples.html
# https://spdx.org/licenses/

# * 成功: MIT, MIT License, Apatch 2.0
# * 取得できず: BSD, BSD-Like, Simplified BSD, LGPL
# * 間違い: BSD License(Unlicenseになる)
# * 未確認: CC0等上記以外すべて
class UseLibLicense:
    def __init__(self, args):
        self.__args = args
        self.__config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        self.__path_dir_root = pathlib.Path(__file__).resolve().expanduser().parent.parent
        self.__path_file_config = None
        
    def GetMarkdownTable(self):
        self.__LoadConfig()
        self.__licenseDbPath = self.__RaiseLoadLicenseDbPath()
        return self.__MetadataToMdTable(self.__ReadMetadata(self.__GetModuleDirs()))

    def __GetModuleDirs(self):
        # ~/root/env/py/auto_github/lib/python3.6/site-packages
        site_packages = []
        import pkgutil
        for m in pkgutil.iter_modules():
            if m.module_finder.path.endswith('/site-packages'):
                if 0 == len(site_packages): site_packages.append(m)
                elif 0 < len(site_packages) and site_packages[0].module_finder.path != m.module_finder.path: site_packages.append(m)
        return site_packages

    def __ReadMetadata(self, site_packages):
        metadatas = []
        from distutils.dist import DistributionMetadata
        for m in site_packages:
            for p in pathlib.Path(m.module_finder.path).glob('*-info'):
                if not p.is_dir(): continue
                for f in ['PKG-INFO', 'METADATA']:
                    filepath = (p / f)
                    if filepath.is_file():
                        with filepath.open() as metafile:
                            metadata = DistributionMetadata()
                            metadata.read_pkg_file(metafile)
                            metadatas.append(metadata)
        return metadatas

    def __MetadataToMdTable(self, metadatas):
        with io.StringIO() as buf:
            crs = CopyRightSearcher()
            for m in metadatas:
                if m.license is None:
                    print('*************** license が None. {}'.format(m.name))
                    continue
                buf.write('[' + m.name + ' ' + m.version + ']' + '(' + m.url  + ' ' + '"' + m.description + '"' + ')')
                
                license_url = self.__GetSameLicenseUrl(m.license)
                if license_url is None: buf.write('|' + m.license)
                else: buf.write('|' + '[' + m.license + ']' + '(' + license_url + ')')
                buf.write('|' + 'Copyright (c) ' + '{0:%Y}'.format(datetime.datetime.now()) + ' ' + m.author)
                copyright = crs.Search(m)
                if copyright is None: buf.write('|' + m.author if m.author is not None else '')
                else: buf.write('|' + copyright)
                buf.write('\n')
            return buf.getvalue()

    def __GetLicenseNames(self):
        conn = sqlite3.connect(str(self.__licenseDbPath))
        cur = conn.cursor()
        cur.execute("select Key, Name, HtmlUrl, Url, SpdxId from Licenses order by Name asc;".format(self.__args.license))
        res = cur.fetchall()
        return res

    def __GetSameLicenseUrl(self, metadata_license):
        meta_lic = re.sub(r' Licen[c|s]e$', '', metadata_license).lower()
        lnames = self.__GetLicenseNames()
        import difflib
        # Licenses.Key と比較
        for record in lnames:
            if meta_lic == record[0].lower():
                return self.__MakeLicenseUrl(record)

        res = [(record, difflib.SequenceMatcher(a=meta_lic, b=record[0].lower()).ratio()) for record in lnames]
        res = sorted(res, key=lambda item: item[1], reverse=True)
        #for r in res: print(metadata_license, r[1], r[0][0])
        if res[0][1] < 0.7: return None # 一致率が60%未満の場合、不一致とみなす
        else:
            # 一致率が最も高いもの
            return self.__MakeLicenseUrl(res[0][0])

    def __MakeLicenseUrl(self, record):
        if record[2] is not None and '' != record[2].strip():
            return record[2] # License.HtmlUrl
        elif record[3] is None or '' == record[3].strip():
            return record[3] # License.Url
        else:
            return "https://opensource.org/licenses/" + record[4] # License.SpdxId

    def __LoadConfig(self):
        for f in [self.__path_dir_root / 'res/repo.ini']:
            if os.path.isfile(f):
                self.__path_file_config = f
                self.__config.read(str(f))
                return
        raise Exception('repo.iniファイルが存在しません。')
       
    def __RaiseLoadLicenseDbPath(self):
        if 'Db' not in self.__config.sections(): raise Exception('Dbセクションがありません。file={}'.format(self.__path_file_config))
        if 'Licenses' not in self.__config['Db']: raise Exception('DbセクションにLicensesキーがありません。LicensesDBファイルパスを指定してください。file={}'.format(self.__path_file_config))
        if '' ==  self.__config['Db']['Licenses'].strip(): raise Exception('DbセクションのLicensesキーに値がありません。LicensesDBファイルパスを指定してください。file={}'.format(self.__path_file_config))
        return pathlib.Path(self.__config['Db']['Licenses']).expanduser().resolve()

if __name__ == '__main__':
    UseLibLicense(None).Write()

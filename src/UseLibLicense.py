#!python3
#encoding:utf-8
import os.path, pathlib
import argparse, configparser
import sqlite3
import datetime
import io
import re

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
        """
        path = os.path.join(self.__args.output_dir, 'LICENSE.txt')
        if os.path.isfile(path):
            print('LICENSE.txtが既存のため作成は中止します。')
            return
        
        self.__LoadConfig()
        licenseDbPath = self.__RaiseLoadLicenseDbPath()
        record = self.__SelectLicense(licenseDbPath )
        if record is None: raise Exception("指定されたライセンス'{}'はDBに存在しません。DBに存在するライセンスは次のとおりです。{}".format(self.__args.license, self.__SelectAllKeys(licenseDbPath )))
        
        source = self.__Replace(record[0])
        with open(path, 'w') as f: f.write(source)
        """
        self.__LoadConfig()
        self.__licenseDbPath = self.__RaiseLoadLicenseDbPath()
        return self.__MetadataToMdTable(self.__ReadMetadata(self.__GetModuleDirs()))

    def __GetModuleDirs(self):
        # /home/pi/root/env/py/auto_github/lib/python3.6/site-packages
        #path = path_root_venv / 'lib/python*/site-packages'
        site_packages = []
        import pkgutil
        for m in pkgutil.iter_modules():
            if m.module_finder.path.endswith('/site-packages'):
                #print(m.name, m.module_finder.path)
                #print(m.name, m.module_finder.path, dir(m))
                if 0 == len(site_packages): site_packages.append(m)
                elif 0 < len(site_packages) and site_packages[0].module_finder.path != m.module_finder.path:
                    site_packages.append(m)
            #print(m.module_finder, dir(m.module_finder))
            #print(m)
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
                        #print(filepath)
                        with filepath.open() as metafile:
                            metadata = DistributionMetadata()
                            metadata.read_pkg_file(metafile)
                            #print(dir(metadata))
                            metadatas.append(metadata)
        return metadatas

    def __MetadataToMdTable(self, metadatas):
        with io.StringIO() as buf:
            for m in metadatas:
                buf.write('[' + m.name + ' ' + m.version + ']' + '(' + m.url  + ' ' + '"' + m.description + '"' + ')')
                if m.license is None:
                    print('*************** license が None. {}'.format(m.name))
                    continue
                license_url = self.__GetSameLicenseUrl(m.license)
                if license_url is None: license_url = ''
                buf.write('|' + '[' + m.license + ']' + '(' + license_url + ')')
                buf.write('|' + '[' + 'Copyright (c) ' + '{0:%Y}'.format(datetime.datetime.now()) + ' ' + m.author + ']' + '(' + '' + ')')
                buf.write('\n')
            return buf.getvalue()

    def __GetLicenseNames(self):
        #self.__LoadConfig()
        #licenseDbPath = self.____RaiseLoadLicenseDbPath()
        conn = sqlite3.connect(str(self.__licenseDbPath))
        cur = conn.cursor()
        cur.execute("select Key, Name, HtmlUrl, Url, SpdxId from Licenses order by Name asc;".format(self.__args.license))
        res = cur.fetchall()
        return res

    def __GetSameLicenseUrl(self, metadata_license):
        lnames = self.__GetLicenseNames()
        import difflib
        # Licenses.Key と比較
        #for record in lnames:
        #    #print(metadata_license, record[0])
        #    s = difflib.SequenceMatcher(a=metadata_license.lower(), b=record[0].lower()).ratio()
        for record in lnames:
            #if metadata_license.lower() == record[0].lower(): return self.__MakeLicenseUrl(record)
            if re.sub(r' Licen[c|s]e$', '', metadata_license).lower() == record[0].lower():
                return self.__MakeLicenseUrl(record)
            #if metadata_license.lower() == record[0].replace(r' Licen[c|s]e$', '').lower(): return self.__MakeLicenseUrl(record)

        res = [(record, difflib.SequenceMatcher(a=metadata_license, b=record[0]).ratio()) for record in lnames]
        res = sorted(res, key=lambda item: item[1], reverse=True)
        #print(metadata_license, res[0])
        #print(res)
        for r in res: print(metadata_license, r[1], r[0][0])
        if res[0][1] < 0.6: return None # 一致率が60%未満の場合、不一致とみなす
        else:
            # 一致率が最も高いもの
            return self.__MakeLicenseUrl(res[0][0])
            #if res[0][0][2] is not None and '' != res[0][0][2].strip():
            #    return res[0][0][2] # License.HtmlUrl
            #elif res[0][0][3] is None or '' == res[0][0][3].strip():
            #    return res[0][0][3] # License.Url
            #else:
            #    return "https://opensource.org/licenses/" + res[0][0][4] # License.SpdxId

        """
        max([difflib.SequenceMatcher(isjunk=lambda item: True if 'Other' == item else False, metadata_license, record[0]).ratio() for record in lnames])

        for record in lnames:
            s = difflib.SequenceMatcher(isjunk=lambda item: True if 'Other' == item else False, metadata_license, record[1]).ratio()
        for n in res:

        conn.close()
        return res
        """

    def __MakeLicenseUrl(self, record):
        if record[2] is not None and '' != record[2].strip():
            return record[2] # License.HtmlUrl
        elif record[3] is None or '' == record[3].strip():
            return record[3] # License.Url
        else:
            return "https://opensource.org/licenses/" + record[4] # License.SpdxId

    def __LoadConfig(self):
        for f in [self.__path_dir_root / 'res/repo.ini']:
            #print(f)
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
        elif author is not None:
            res = source.replace('[year]', '{0:%Y}'.format(datetime.datetime.now()))
            return res.replace('[fullname]', author)
        else:
            return source.replace('[year]', '{0:%Y}'.format(datetime.datetime.now()))
    """


if __name__ == '__main__':
    UseLibLicense(None).Write()

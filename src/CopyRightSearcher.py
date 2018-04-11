#!python3
#encoding:utf-8
import sys, os.path, pathlib
sys.path.append(os.path.expanduser('~/root/_meta/path'))
from PathIni import PathIni
import io
import re
from distutils.dist import DistributionMetadata
import urllib.request, urllib.parse
import csv
import time

# 使用ライブラリのライセンス情報からCopyright情報を探す。
# URLがgithubのとき、LICENSE.txtなどのファイルを探し、その中からCopyRight文字列を探す。
class CopyRightSearcher:
    def __init__(self):
        self.__pattern1 = re.compile(r'.*Copyright[ ]*(© |\([C|c]\))?[ ]*[0-9]{4,}.*')
        self.__pattern2 = re.compile(r'.*(© |\([C|c]\))[ ]*[0-9]{4,}.*')
        self.__path_cache = pathlib.Path(__file__).parent / 'url_cache.tsv'
        self.__LoadCache()

    def Search(self, metadata:DistributionMetadata):
        license_url, copyright = self.__FindLicenseUrlFromCache(metadata)
        if license_url is None: return self.__Search(metadata)
        elif '' == license_url: return (None, None) # cacheにあるが昔探して見つけられなかった
        elif license_url is not None: return (license_url, copyright)  # cacheにある

    def __Search(self, metadata:DistributionMetadata):
        base_url = self.__GetSearchUrl(metadata)
        for fn in self.__GetLicenseFileName():
            try:
                url = base_url.rstrip('/') + '/' + fn.lstrip('/')
                print(url)
                time.sleep(1)
                with urllib.request.urlopen(url) as res:
                    copyright = self.__FindCopyrightString(res.read().decode('utf-8'))
                    self.__AppendCache(metadata, url, copyright if copyright is not None else '')
                    return (url, copyright)
            except urllib.error.HTTPError as e: continue
            except:
                import traceback
                traceback.print_exc()
        self.__AppendCache(metadata, '', '')
        return (None, None)

    # LICENSEファイルがありそうなURL
    # サイトによって違う？: 
    #   bitbucket: https://bitbucket.org/zzzeek/alembic/raw/a7164ef76729aa9306f9c7e2636448a588f35ddb/LICENSE
    #   リビジョンhash値のせいでURLを特定できない
    def __GetSearchUrl(self, metadata:DistributionMetadata):
        url = urllib.parse.urlparse(metadata.url)
        #'https://raw.githubusercontent.com/pallets/markupsafe/master/LICENSE'
        if 'github.com' == url.netloc:
            url_path = url.path.rstrip('/') + '/' + 'master'
            new_url = urllib.parse.urlunparse((url.scheme,'raw.githubusercontent.com',url_path,'','',''))
            print(new_url)
            return new_url
        else:
            for u in [metadata.name, '']:
                try:
                    url = urllib.parse.urljoin(metadata.url, u)
                    with urllib.request.urlopen(url) as res:
                        print('*', url)
                        return url
                except: pass

    def __GetLicenseFileName(self):
        for fn in ['LICENSE', 'COPYING', 'COPYRIGHT', 'LICENCE']:
            for ext in ['', '.txt', '.md']:
                yield fn + ext

    def __GetPathCache(self):
        for path in [PathIni()['root_db_template_command_repo'], pathlib.Path(__file__).parent, pathlib.Path(__file__).parent.parent / 'res']:
            filepath = path / 'url_cache.tsv'
            if filepath.is_file(): return filepath
        
    def __LoadCache(self):
        if not self.__path_cache.is_file():
            self.__path_cache.touch()
        with open(self.__path_cache) as f:
            self.__tsv = list(csv.reader(f, delimiter='\t'))

    # LicenseURLとCopyrightを返す
    def __FindLicenseUrlFromCache(self, metadata):
        for r in self.__tsv:
            if metadata.name == r[0]: return r[1], r[2]
        return None

    def __AppendCache(self, metadata, license_url, copyright):
        if self.__FindLicenseUrlFromCache(metadata) is None:
            with open(self.__path_cache, 'a') as f:
                f.write('\t'.join([metadata.name, license_url, copyright]) + '\n')
            self.__tsv.append([metadata.name, license_url, copyright])

    def __FindCopyrightString(self, text):
        print(text)
        m = self.__pattern1.match(text)
        if m is not None:
            print(m)
            return m[0]
        m = self.__pattern2.match(text)
        if m is not None:
            print(m)
            return m[0]
        return None
        # Copyright YYYY
        # Copyright ©  YYYY
        # Copyright (C) YYYY
        # Copyright (c) YYYY
        # ©  YYYY
        # (C) YYYY
        # (c) YYYY
        # Copyright YYYY
        # Copyright YYYY

import pathlib
import os, os.path
import string

class TemplateRenderer:
    def __init__(self): pass
    def Render(self, tpl_src, **kwargs):
        source = tpl_src
        if ((type(tpl_src) == str or issubclass(type(tpl_src), os.PathLike)) and os.path.isfile(tpl_src)):
            with open(tpl_src) as f:
                source = f.read()
        elif type(tpl_src) != str: raise ValueError('引数tpl_srcはテキストファイルパスかテンプレート文字列にしてください。')
        return self.DoubleCurlyBracketTemplate(source).safe_substitute(**kwargs)

    # {{ }} 中の空白無視
    class DoubleCurlyBracketTemplate(string.Template):
        pattern = r'''
        \{\{[ ]*(?:
        (?P<escaped>\{\{[ ]*)|
        (?P<named>[_a-zA-Z][_a-zA-Z0-9]*)[ ]*\}\}|
        (?P<braced>[_a-zA-Z][_a-zA-Z0-9]*)[ ]*\}\}|
        (?P<invalid>)
        )
        '''
        # 引数が渡されなかった時の置換方法
        # None: 置換しない（プレースホルダそのまま）
        # '': 空文字列
        #default_value = None
        #class DefaultMethod:
        #    def Get(self): return 


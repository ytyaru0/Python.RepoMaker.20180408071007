# 構造

* ~/.bashrc
    * python3 ~/root/script/_meta/path/IniToSh.py
    * . ~/root/script/_meta/path/sh/paths.sh
* ~/root/
    * _meta/
        * path/
            * ini/
                * path.ini
            * sh/
                * paths.sh
            * IniToSh.py
        * command/
            * do/
                * setup_complete_candidate.sh
                * command_replace.tsv
            * pj/
                * setup_complete_candidate_pj.sh
                * categoly_root.list
            * repo/
    * script/
        * sh/
            * _command/
                * do
        * py/
            * os/file/
                * NameGenerator.py
            * _command/
                * do/
                    * TemplateMaker/
                        * CommandReplaceFile.py
                        * CommandsFile.py
                        * CommandToTemplate.py
                        * ConfigFile.py
                        * do.py
                        * GetCompleteCandidate.py
                        * PathToCommand.py
                * pj/
                * repo/

* ~/root/db/
    * meta/
        * programming/
            * [languages.yml](https://raw.githubusercontent.com/github/linguist/master/lib/linguist/languages.yml)
            * GitHub.License.sqlite3
    * template/
        * _command/
            * do/
                * py/
                    * 2/
                    * 3/
                        * Context/
                            * hello.py
            * pj/
                * categoly.list
                * py/
                * sh/
                * html/
                    * blog
            * repo/

* /tmp/work/.meta/
    * _command/
        * repo/

* https://github.com/{user}/Aggregate
    * 集計データをUP,集約するリポジトリ

## RAM Disk

`/tmp/`はRAMディスクとする。
テンプレートが追加されるなどの変更があっても、tsvファイルの変更はメモリ上で保持される。SDカードやSSDへの書込は生じない。

## Python

repoコマンドはshellでなくPython主体で実装されている。

よって、実行前にはPython設定スクリプトが必要。

* /tmp/work/RaspberryPi.Home.Root.20180318143826/src/script/sh/_called/bash/bashrc.sh

```sh
# 時刻同期できない問題: .bash_profileだとログイン後に自動実行されるが時刻同期されず。一時ファイルだけが作成されて以降実行されなくなってしまう。
. "$HOME/root/script/sh/_lib/env.sh"
ExportPath "$HOME/root/tool" "$HOME/root/script/sh/_command"
. ~/root/script/sh/mkdir_work.sh
~/root/script/sh/call_settime.sh
. ~/root/script/sh/pyenv.sh
. ~/root/script/sh/py_venv.sh

# ユーザパス設定読込
python3 /tmp/work/RaspberryPi.Home.Root.20180318143826/src/_meta/path/IniToSh.py
. /tmp/work/RaspberryPi.Home.Root.20180318143826/src/_meta/path/sh/paths.sh
#python3 ~/root/_meta/path/IniToSh.py
#. ~/root/_meta/path/sh/paths.sh

# コマンドの引数補完セット
. /tmp/work/RaspberryPi.Home.Root.20180318143826/src/_meta/command/do/setup_complete_candidate_do.sh
#. /tmp/work/Python.TemplateFileMaker.20180314204216/src/setup_complete_candidate_do.sh
#. ~/root/_meta/command/setup_complete_candidate_do.sh
```

### テンプレートエンジン

jinja2を使う。これに伴い、repoコマンド実行には仮想環境のactivateが必要。

* `~/root/env/py/template/bin/activate`

repoコマンドスクリプト内で呼び出す。

* ~/root/script/sh/_command/repo
* /tmp/work/RaspberryPi.Home.Root.20180318143826/src/script/sh/_command/repo

## 名前

ファイル、ディレクトリ、セクション、キー、変数などの名前をどうするか。

### 複数形

複数形は使わない。`templates`にすべきと思ったが、`command`も`commands`にしなければならない。libもlibrariesに, `script`も`scripts`にせねば。むしろ、すべて複数形ではないか？ 

複数形にすると統一性が保てなくなる。s, esなどもそうだし、indexはindicesになる。もはや元型が崩れる。悩むので使わない。

でも、`root.ini`のセクション名は`Paths`とする。`Path`は既存の環境変数名とかぶるから。shell文脈の都合により、統一できない。

### erとor

creater, creator, で悩む。前者は英語、後者は米語らしいが、単語によって変わったりもするらしい。統一性が保てない。すでに`NameGenerator`などで使ってしまった。

クラス名やモジュール名ではよく使う。`er`, `or`をやめた名詞にすべき？`NameGenerator`は`Name`と`Generate()`にすれば解決する、か？ `NameSequencer.Generate()`とかにしたくなる。ただの名前でなくて連番名なので`SequenceName.Generate()`がいいか？

http://tak-shonai.cocolog-nifty.com/crack/2013/09/-er--or-b920.html

### 大文字と小文字

* Linux FileSystem
    * 区別する。設定で区別しないようにもできると思う
* Ini (Pythonのconfigparser)
    * Section: 区別する
    * Key: 区別しない

統一できない。


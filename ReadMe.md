# このソフトウェアについて

リポジトリに必要なReadMe.md, LICENSE.txtなどを作成する。

# 目的

コードを書くとき、`src`, `res`, `test`, `lib`, のようなディレクトリ構造をつくることがある。お決まりなのに毎回作成するのは面倒なので。

* ReadMe.md
* LICENSE.txt
* .git
* .gitignore
* Git
    * Commit
        * Message
* GitHub Repo
    * Create
        * Description
        * Homepage

# 使い方

コマンド策定中。

[command_name.md](memo/command_name.md)

ヘルプ表示。
```sh
python3 RepoMaker.py
```

指定ディレクトリにReadMe.mdやLICENSE.txtなどを作成。
```sh
python3 RepoMaker.py {dirpath}
```

ローカルリポジトリ作成。
```sh
python3 RepoMaker.py {dirpath} {username}
```

リモートリポジトリ作成。
```sh
python3 RepoMaker.py {dirpath} {username} {description}
```

ライセンスをデフォルトのCC0-1.0ではなく指定のものにする。
```sh
python3 RepoMaker.py {dirpath} {username} {description} -l {license}
```

コミットメッセージをdescriptionとは別にする。
```sh
python3 RepoMaker.py {dirpath} {username} {description} -m {commit-message}
```

コミットメッセージをdescriptionとは別にする。
```sh
python3 RepoMaker.py {dirpath} {username} {description} {commit-message}
```

# できたらいいな

* ReadMe.md
    * 概要の一文をGitHub Repo Descriptionと同じにする
* LICENSE.txt
    * copyrightの西暦をリアルタイム出力
    * 著者名は何もなければgithub usernameと同じ
* SourceCode
    * GPLv3などソースコードごとにライセンスコメントが必要な場合、自動追加する
    * 利用しているパッケージを自動チェックしてライセンス表記を作成したい
        * python
            * `import`文、`pip list`などから自動取得できないか
* .git
    * username
    * mailaddress
    * 通信方法(HTTPS/SSH)
    * CommitMessage
* GitHub
    * Create Repo
        * description
        * homepage
* Mastodon
    * Toot
        * text: description
        * hash: language, license
* hatena-blog
    * テンプレ出力
        * タイトルは{description}と同一
    * APIで下書きをPOST
* 集計
    * Repository
        * 日時
        * URL(username, reponame)
        * 言語ごとのコード量(Byte)
        * CommitId
        * Commitごとの編集量(Line(insert,delete))

# 関係リポジトリ

リポジトリ|説明
----------|----
[Python.TemplateFileMaker.20180314204216](https://github.com/ytyaru0/Python.TemplateFileMaker.20180314204216)|単一ファイルを出力する
[Python.ProjectMaker.20180402173000](https://github.com/ytyaru0/Python.ProjectMaker.20180402173000)|プロジェクト一式を出力する
[RaspberryPi.Home.Root.20180318143826](https://github.com/ytyaru0/RaspberryPi.Home.Root.20180318143826)|上記コマンドを含んだスクリプト一式

# 開発環境

* [Raspberry Pi](https://ja.wikipedia.org/wiki/Raspberry_Pi) 3 Model B
    * [Raspbian](https://www.raspberrypi.org/downloads/raspbian/) GNU/Linux 8.0 (jessie)
        * [pyenv](http://ytyaru.hatenablog.com/entry/2019/01/06/000000)
            * Python 3.6.4

# ライセンス

このソフトウェアはCC0ライセンスである。

[![CC0](http://i.creativecommons.org/p/zero/1.0/88x31.png "CC0")](http://creativecommons.org/publicdomain/zero/1.0/deed.ja)


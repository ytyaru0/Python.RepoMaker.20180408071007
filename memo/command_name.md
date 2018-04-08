# コマンド名

指定ディレクトリにReadMe.mdなどリポジトリに必要な一式を作成する。

```
$ repo {dirpath} {username} {description} {commit-message}
```

引数が多すぎて位置と内容を覚えられない。キーワード引数にしてみる場合、以下のようなパターンが考えられる。

```
$ repo {dirpath} {username} {description} -m {commit-message} -l {license}
```

```
$ repo {dirpath} -u {username} -d {description} -m {commit-message} -l {license}
```

`-e`はライセンスコメントを埋め込む対象を指定する。
```
$ repo {dirpath} -u {username} -d {description} -m {commit-message} -l {license} -e {extension}
```

`-s`はgit pushするときの通信方法。`~/.ssh/config`にあるホスト名を指定する。あればSSH通信、なければHTTPS通信。
```
$ repo {dirpath} -u {username} -d {description} -m {commit-message} -l {license} -e {extension} -s {ssh-host}
```

`-h`はGitHub Repo のhomepage。なければ設定しないか設定したメソッドにより決定する。HatenaBlogのAPI投稿と連動させたい。
```
$ repo {dirpath} -u {username} -d {description} -m {commit-message} -l {license} -e {extension} -s {ssh-host} -h {homepage}
```

位置引数{dirpath}を省略するとカレントディレクトリが対象になる。
```
$ repo -u {username} -d {description} -m {commit-message} -l {license} -e {extension} -s {ssh-host} -h {homepage}
```

カレントディレクトリに`.meta/repo.sh`が存在し、内容が`repo`コマンドであれば、それを実行する。
```sh
$ repo
```
./.meta/repo.sh
```sh
repo -u {username} -d {description} -m {commit-message} -l {license} -e {extension} -s {ssh-host} -h {homepage}
```

`-e`が多い場合など、覚えていられないことがありうるので。また、サブコマンド`change`を使うときに前回の値を参照できるようにしておきたい。

## サブコマンド

ライセンスの年号を更新する。ライセンスコメントがないソースコードがあれば追記する。
```
$ repo update ...
```

指定した項目を指定値に変更する。
```
$ repo change ...
```

### update

コミットメッセージは指定がない限り`$ repo update`というコマンドそのまま。または設定によりデフォルト値を変更できる。

repo.ini
```ini
[Update]
CommitMessage=ライセンス表記の更新
```

### change

`-d`, `-h`を対象とする。GitHub APIで変更できる。

`-l`は実装したいのだが、大変そう。既存のライセンスコメントと一致するか否かの判定が必要。存在すれば、その部分を新しいものに置換するなり、不要なら削除する。LICENSE.txtも新しい物にし、ReadMe.mdも変える。

`-u`は変更してしまうと大事になる。前回のリポジトリを削除し、今回のユーザに同名のリポジトリを新規作成することになる。そもそも、そんな要求自体が少ないと思うし、移動先で同名のリポジトリが既存だった場合など、面倒が多い。よって`-u`は`change`の対象外。

`-s`はそもそも開発環境であるRaspberryPiでは`HTTPS`による通信しかできていない。たぶん`.git/config`のURLを変更すれば良いのだと思うが、対象外とする。

`-m`はどの時点でのメッセージを変更するのか指定せねばならない。面倒なのでgitコマンドでやってもらいたい。方法は知らない。

`-e`はコマンド実行する都度、指定すればいいだけ。`.meta/repo.sh`のファイル内を直接変更してもいい。わざわざこのコマンドで指定する必要なし。

## 他サービス連携

* GitHub
* Mastodon
* Hatena Blog

この辺は別プロジェクトにすべきかもしれない。

ただ、コマンド引数との関係だけは定めておきたい。

### Hatena Blog

`-h`はGitHub Repo のhomepage。なければ設定しないか設定したメソッドにより決定する。HatenaBlogのAPI投稿と連動させたい。
```
$ repo {dirpath} -u {username} -d {description} -m {commit-message} -l {license} -e {extension} -s {ssh-host} -h {homepage}
```



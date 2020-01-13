# JsonKeyList
JSONからkey一覧を生成します。APIのインターフェースを整理する時に必要だったので作ってみました。
## Sample
下記のようにJSONからキーの一覧を取得できます。JSON PATH 形式で値にアクセスする機能は用意していませんが、その機能を使うPGの設計書を作るときとかに使えるかと思います。
  
JSON
```
{
  "sample": {
    "simple_value": "simple_value",
    "list": [
      "list_value01",
      "list_value02"
    ],
    "object": {
      "object_value":  "object_value"
    }
  }
}
```
結果
```
###obj###.sample
###obj###.sample.simple_value
###obj###.sample.list
###obj###.sample.list.###list_index[0]###
###obj###.sample.list.###list_index[1]###
###obj###.sample.object
###obj###.sample.object.object_value
```

実際にはdictを受け取って、keyを書き換えたdictを返却しているので、valueも取得可能です。valueについてはobjectやlistの場合は{}とか[]に置き換えるオプションも用意しています。
また、先頭の「###obj###」は任意の文字列に置き換えたり、カットすることも可能です。
```
sample : {}
sample.simple_value : simple_value
sample.list : []
sample.list.###list_index[0]### : list_value01
sample.list.###list_index[1]### : list_value02
sample.object : {}
sample.object.object_value : object_value
```
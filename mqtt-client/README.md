# 進捗

## 12/4

1. ドキュメントを読んでpaho.mqtt.publish/subscribe と paho.mqtt.clientの違いを理解した.　
2. MQTTでwhile文でQueryを受け取れるようになった.

# TODO

1. Queryを受け取った後のRaspiの処理を進める
    1. センサで情報取得
    2. Queryに基づいて符号化&点灯

2. Decoder側の処理を進める
    1. EncoderにQueryを送れることを確認 & whileでloopしているので一旦起動すればok.
    2. Queryを送った後に、全点灯&全消灯を行う -> Decoder側で撮影.
    3. 格納してEncoderの場所を保存する.
    4. あとはひたすらDOCを行う.

## 12/5

### 備考
今の形式だと、publisherはSubscriberのIP addressを知らなくても通信可能になっている→BrokerのIP addressさえ知っていれば通信可能.

非同期通信はどうするか?→最終のtopicをスタックしておいて、Encoderが定期的に読みに行く形がいいかも? -> 常に```retain```の設定でpublishする.->
```retain=True```にしたことで、Encoderがいつでも取り出せるようにできた

Brokerが蓄えている情報をみたい?

最後に各符号器が符号化したセンサデータをPublish, DecoderでSubscribeして復号結果との整合性を確認する.
